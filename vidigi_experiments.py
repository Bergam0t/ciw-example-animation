import plotly.graph_objects as go
import pandas as pd
from pathlib import Path

# Import the wrapper objects for model interaction.
from ciw_model import Experiment, multiple_replications

N_OPERATORS = 13
N_NURSES = 9
RESULTS_COLLECTION_PERIOD = 1000

user_experiment = Experiment(n_operators=N_OPERATORS,
                                     n_nurses=N_NURSES,
                                     chance_callback=0.4)

# run multiple replications
results, logs = multiple_replications(user_experiment, n_reps=10)

# the 'logs' object contains 1

logs_run_1 = logs[0]

print(len(logs_run_1))

# [print(log) for log in logs_run_1]

# let's print all of the outputs for a single individual
[print(log) for log in logs_run_1 if log.id_number==500]

# if we know the nodes and what wthey relate to, we can build up a picture
# the arrival date for the first tuple for a given user ID is the arrival

# then, for each node:
# the arrival date for a given node is when they start queueing
# the service start date is when they stop queueing
# the service start date is when they begin using the resource
# the service end date is when the resource use ends
# the server ID is a resource use ID


def event_log_from_ciw_recs(ciw_recs_obj, node_name_list):
    """
    Given the ciw recs object, return a dataframe
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

    # return patient_ids

print(event_log_from_ciw_recs(logs_run_1, node_name_list=["operator", "nurse"]))

event_log_test = event_log_from_ciw_recs(logs_run_1, node_name_list=["operator", "nurse"])

from vidigi.animation import animate_activity_log

# placeholder - function that can run this for a list of multiple rec objects

event_position_df = pd.DataFrame([
                    {'event': 'arrival',
                     'x':  50, 'y': 300,
                     'label': "Arrival" },

                    {'event': 'operator_wait_begins',
                     'x':  205, 'y': 170,
                     'label': "Waiting for Operator"},

                    {'event': 'operator_begins',
                     'x':  205, 'y': 110,
                     'resource':'n_operators',
                     'label': "Speaking to operator"},

                    {'event': 'nurse_wait_begins',
                     'x':  205, 'y': 270,
                     'label': "Waiting for Nurse"},

                    {'event': 'nurse_begins',
                     'x':  205, 'y': 210,
                     'resource':'n_nurses',
                     'label': "Speaking to Nurse"},

                    {'event': 'exit',
                     'x':  270, 'y': 70,
                     'label': "Exit"}

                ])

class model_params():
    n_operators = N_OPERATORS
    n_nurses = N_NURSES

animate_activity_log(
        event_log=event_log_test,
        event_position_df= event_position_df,
        scenario=model_params(),
        debug_mode=True,
        every_x_time_units=1,
        include_play_button=True,
        icon_and_text_size=20,
        gap_between_entities=6,
        gap_between_rows=15,
        plotly_height=700,
        frame_duration=200,
        plotly_width=1200,
        override_x_max=300,
        override_y_max=500,
        limit_duration=RESULTS_COLLECTION_PERIOD,
        wrap_queues_at=25,
        step_snapshot_max=125,
        time_display_units="dhm",
        display_stage_labels=True,
    )
