from draw_chap06_fig_envelope_point_comparison import draw as draw_envelope_point_comparison
from draw_chap06_fig_local_planner_architecture import draw as draw_local_planner_architecture
from draw_chap06_fig_rolling_mpc_flow import draw as draw_rolling_mpc_flow


def main():
    draw_local_planner_architecture()
    draw_envelope_point_comparison()
    draw_rolling_mpc_flow()


if __name__ == "__main__":
    main()
