import pandas as pd

def event_log_from_ciw_recs(ciw_recs_obj, node_name_list):
    """
    Given the ciw recs object, return a dataframe

    if we know the nodes and what they relate to, we can build up a picture
    the arrival date for the first tuple for a given user ID is the arrival

    then, for each node:
    the arrival date for a given node is when they start queueing
    the service start date is when they stop queueing
    the service start date is when they begin using the resource
    the service end date is when the resource use ends
    the server ID is a resource use ID

    """
    entity_ids = list(set([log.id_number for log in ciw_recs_obj]))

    event_logs = []

    for entity_id in entity_ids:
        entity_tuples = [log for log in ciw_recs_obj if log.id_number==entity_id]

        total_steps = len(entity_tuples)

        # If first entry, record the arrival time
        for i, event in enumerate(entity_tuples):
            if i==0:
                event_logs.append(
                    {'patient': entity_id,
                    'pathway': 'Model',
                    'event_type': 'arrival_departure',
                    'event': 'arrival',
                    'time': event.arrival_date}
                )

            event_logs.append(
            {'patient': entity_id,
             'pathway': 'Model',
             'event_type': 'queue',
             'event': f"{node_name_list[i]}_wait_begins",
             'time': event.arrival_date
                }
            )

            event_logs.append(
                {'patient': entity_id,
                'pathway': 'Model',
                'event_type': 'resource_use',
                'event': f"{node_name_list[i]}_begins",
                'time': event.service_start_date,
                'resource_id': event.server_id}
            )

            event_logs.append(
                {'patient': entity_id,
                'pathway': 'Model',
                'event_type': 'resource_use',
                'event': f"{node_name_list[i]}_ends",
                'time': event.service_end_date,
                'resource_id': event.server_id}
            )


            if i==total_steps-1:
                event_logs.append(
                    {'patient': entity_id,
                    'pathway': 'Model',
                    'event_type': 'arrival_departure',
                    'event': 'depart',
                    'time': event.exit_date}
                )

    return pd.DataFrame(event_logs)



# placeholder - function that can run this for a list of multiple rec objects
