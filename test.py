from prefect.deployments import Deployment
from flow import GCS_to_BQ_ETL  # import your flow function

deployment = Deployment.build_from_flow(
    flow=GCS_to_BQ_ETL,
    name="GCS → BQ ETL",
    parameters={},  # add parameters here if needed
)

if __name__ == "__main__":
    deployment.apply()