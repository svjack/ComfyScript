import json
from types import SimpleNamespace
import networkx as nx

from . import astutil

class WorkflowToScriptTranspiler:
    def __init__(self, workflow: str):
        workflow = json.loads(workflow, object_hook=lambda d: SimpleNamespace(**d))
        assert workflow.version == 0.4

        G = nx.MultiDiGraph()
        for node in workflow.nodes:
            # TODO: Directly add node?
            G.add_node(node.id, v=node)
        
        links = {}
        for link in workflow.links:
            (id, u, u_slot, v, v_slot, type) = link
            G.add_edge(u, v, key=id, u_slot=u_slot, v_slot=v_slot, type=type)
            links[id] = (u, v, id)
        
        self.G = G
        self.links = links

    def _declare_id(self, id: str) -> str:
        if id not in self.ids:
            self.ids[id] = {}
        return id

    def _assign_id(self, name: str) -> str:
        if name in self.ids:
            i = 2
            while f'{name}{i}' in self.ids:
                i += 1
            name = f'{name}{i}'
        self.ids[name] = {}
        return name

    def _node_to_assign_st(self, node):
        G = self.G
        links = self.links

        v = node['v']
        # print(v.id)

        vars = []
        vars_used = False
        if hasattr(v, 'outputs'):
            # Unused outputs have no slot_index.
            # sort() is stable.
            v.outputs.sort(key=lambda output: getattr(output, 'slot_index', 0xFFFFFFFF))
            for output in v.outputs:
                # Outputs used before have slot_index, but no links.
                if hasattr(output, 'slot_index') and len(output.links) > 0:
                    id = self._assign_id(astutil.str_to_var_id(
                        getattr(v, 'title', '') + output.name if output.name != '' else output.type
                    ))
                    node.setdefault('output_ids', {})[output.slot_index] = id
                    vars_used = True
                else:
                    id = '_'
                vars.append(id)
        
        args = []
        if hasattr(v, 'inputs'):
            v.inputs.sort(key=lambda input: G.edges[links[input.link]]['v_slot'])
            for input in v.inputs:
                (node_u, node_v, link_id) = links[input.link]
                edge = G.edges[node_u, node_v, link_id]
                args.append(G.nodes[node_u]['output_ids'][edge['u_slot']])
        if hasattr(v, 'widgets_values'):
            # https://github.com/comfyanonymous/ComfyUI/blob/2ef459b1d4d627929c84d11e5e0cbe3ded9c9f48/web/extensions/core/widgetInputs.js#L326-L375
            for value in v.widgets_values:
                # `value is str` doesn't work
                if type(value) is str:
                    args.append(astutil.to_str(value))
                else:
                    # int, float
                    args.append(str(value))
        # TODO: If an input is only used by current node, and current node outputs a same type node, then the output should take the input's var name.
        # e.g. Reroute, TomePatchModel

        class_id = self._declare_id(astutil.str_to_class_id(v.type))

        c = ''
        # TODO: Dead code elimination
        if len(vars) > 0 and not vars_used:
            c += '# '
        if len(vars) != 0:
            c += f"{astutil.to_tuple(vars)} = "
        c += f"{class_id}({', '.join(args)})\n"
        return c
    
    def to_script(self) -> str:
        # From leaves to roots or roots to leaves?
        # ComfyUI now executes workflows from leaves to roots, but there is a PR to change this to from roots to leaves with topological sort: https://github.com/comfyanonymous/ComfyUI/pull/931
        # To minimize future maintenance cost and suit the mental model better, we choose **from roots to leaves** too.

        self.ids = {}

        c = ''
        # TODO: Human-readable topological sort
        for node in nx.topological_sort(self.G):
            c += self._node_to_assign_st(self.G.nodes[node])
        return c
    
__all__ = [
    'WorkflowToScriptTranspiler',
]