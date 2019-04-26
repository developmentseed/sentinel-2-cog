"""Lambda_pyskel.scripts.cli."""

import json

import click
from boto3.session import Session as boto3_session


@click.command(short_help="Invoke Lambda")
@click.argument("sceneid", type=str, nargs=1)
@click.option(
    "--bidx", "-b", type=str, multiple=True, help="Band index to copy", required=True
)
@click.option("--stage", type=str, default="production", help="Stack stage")
@click.option("--function", type=str, default="translator", help="Function's name")
@click.option("--region", type=str, default="eu-central-1", help="AWS Lambda region")
def invoke(sceneid, bidx, stage, function, region):
    """Invoke Lambda."""
    function_name = f"sentinel2-to-cog-{stage}-{function}"
    session = boto3_session(region_name=region)
    awslambda = session.client("lambda")
    for b in bidx:
        payload = dict(sceneid=sceneid, band=b)
        awslambda.invoke(
            FunctionName=function_name,
            InvocationType="Event",
            LogType="None",
            Payload=json.dumps(payload),
        )


if __name__ == "__main__":
    invoke()
