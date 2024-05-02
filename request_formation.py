from rdflib import Graph


def get_all_entity_labels_with_limit(ontology_graph):

    all_entity_labels = {}
    entity_counter = 0  # Счетчик для отслеживания количества сущностей с метками

    query_entities = f"""
       SELECT DISTINCT ?entity
       WHERE {{
           ?entity rdfs:label ?label .
       }}
    """
    results_entities = ontology_graph.query(query_entities)

    for row_entity in results_entities:
        entity_uri = row_entity[0]
        labels = get_entity_labels(entity_uri)
        if labels:
            all_entity_labels[entity_uri] = labels
            entity_counter += 1

    print(f"Найдено меток для {entity_counter} сущностей")
    return all_entity_labels


def get_entity_labels(entity_uri):
    labels = set()

    # Получаем все метки для указанной сущности
    query_entity_labels = f"""
       SELECT DISTINCT ?label
       WHERE {{
           <{entity_uri}> rdfs:label ?label .
       }}
    """
    results_entity_labels = g.query(query_entity_labels)

    for row_label in results_entity_labels:
        labels.add(row_label[0])

    return labels


if __name__ == "__main__":
    g = Graph()
    g.parse("OntoMathPro_v2.owl", format="xml")
    all_entity_labels = get_all_entity_labels_with_limit(g)
    if not all_entity_labels:
        print("Не найдено меток для сущностей в онтологии.")
    else:
        for entity_uri, labels in all_entity_labels.items():
            print("Метки сущности", entity_uri, ":", labels)
