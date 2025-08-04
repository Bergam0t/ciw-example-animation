import plotly.graph_objects as go
import pandas as pd
from pathlib import Path

# Import the wrapper objects for model interaction.
from ciw_model import Experiment, multiple_replications
from vidigi.ciw import event_log_from_ciw_recs
from vidigi.animation import animate_activity_log
from vidigi.utils import EventPosition, create_event_position_df

N_OPERATORS = 13
N_NURSES = 9
RESULTS_COLLECTION_PERIOD = 1000

user_experiment = Experiment(n_operators=N_OPERATORS,
                                     n_nurses=N_NURSES,
                                     chance_callback=0.4)

# run multiple replications
results, logs = multiple_replications(user_experiment, n_reps=10)

# the 'logs' object contains a list, where each entry is the recs object for that run
logs_run_1 = logs[0]

print(len(logs_run_1))

# [print(log) for log in logs_run_1]

# let's print all of the outputs for a single individual
[print(log) for log in logs_run_1 if log.id_number==500]

print(event_log_from_ciw_recs(logs_run_1, node_name_list=["operator", "nurse"]))

# let's now try turning this into an event log
event_log_test = event_log_from_ciw_recs(logs_run_1, node_name_list=["operator", "nurse"])

event_log_test.head(25)

# Create required event_position_df for vidigi animation

event_position_df = create_event_position_df([
    EventPosition(event='arrival', x=30, y=350, label="Arrival"),
    EventPosition(event='operator_wait_begins', x=205, y=270, label="Waiting for Operator"),
    EventPosition(event='operator_begins', x=205, y=210, resource='n_operators', label="Speaking to operator"),
    EventPosition(event='nurse_wait_begins', x=205, y=110, label="Waiting for Nurse"),
    EventPosition(event='nurse_begins', x=205, y=50, resource='n_nurses', label="Speaking to Nurse"),
    EventPosition(event='depart', x=270, y=10, label="Exit"),
])
# Create a suitable class to pass in the resource numbers

class model_params():
    n_operators = N_OPERATORS
    n_nurses = N_NURSES

# Create animation

fig = animate_activity_log(
        event_log=event_log_test,
        event_position_df= event_position_df,
        scenario=model_params(),
        debug_mode=True,
        setup_mode=False,
        every_x_time_units=1,
        include_play_button=True,
        entity_icon_size=20,
        text_size=20,
        gap_between_entities=8,
        gap_between_queue_rows=25,
        plotly_height=700,
        frame_duration=200,
        plotly_width=1200,
        override_x_max=300,
        # override_y_max=400,
        limit_duration=RESULTS_COLLECTION_PERIOD,
        wrap_queues_at=25,
        step_snapshot_max=75,
        time_display_units="dhm",
        display_stage_labels=True,
    )

fig.write_html("vidigi_animation_example.html")

fig
