class Registry:
    def __init__(self):
        self._next_entity_id = 0
        self._components = {} # Dict of component_type -> dict of entity_id -> component_instance
        self._entities = set()

    def create_entity(self):
        entity_id = self._next_entity_id
        self._next_entity_id += 1
        self._entities.add(entity_id)
        return entity_id

    def destroy_entity(self, entity_id):
        if entity_id in self._entities:
            self._entities.remove(entity_id)
            for component_type in self._components:
                if entity_id in self._components[component_type]:
                    del self._components[component_type][entity_id]

    def add_component(self, entity_id, component):
        comp_type = type(component)
        if comp_type not in self._components:
            self._components[comp_type] = {}
        self._components[comp_type][entity_id] = component

    def get_component(self, entity_id, component_type):
        if component_type in self._components:
            return self._components[component_type].get(entity_id)
        return None

    def has_component(self, entity_id, component_type):
        return component_type in self._components and entity_id in self._components[component_type]

    def view(self, *component_types):
        """Returns a list of entity_ids that have all the specified component types."""
        if not component_types:
            return []

        # Start with entities of the first component type
        first_type = component_types[0]
        if first_type not in self._components:
            return []

        valid_entities = set(self._components[first_type].keys())

        # Intersect with the rest
        for comp_type in component_types[1:]:
            if comp_type not in self._components:
                return []
            valid_entities.intersection_update(self._components[comp_type].keys())

        return list(valid_entities)

class System:
    def __init__(self, registry):
        self.registry = registry

    def update(self, dt):
        pass
