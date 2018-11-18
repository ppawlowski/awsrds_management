import boto3
import datetime

def rds_snapshot_cleanup():
    rds_client = boto3.client('rds')
    snapshots = rds_client.describe_db_snapshots()
    offset = 7
    calculate_past_date = datetime.datetime.now() - datetime.timedelta(days=offset)
    converted_past_date = calculate_past_date.date()

    for snapshot in snapshots['DBSnapshots']:
        if snapshot['SnapshotCreateTime'].date() <= converted_past_date:
            print('Snapshot ' + snapshot['DBSnapshotIdentifier'] + ' will be deleted.')
            try:
                rds_client.delete_db_snapshot(DBSnapshotIdentifier=snapshot['DBSnapshotIdentifier'])
            except Exception as e:
                print('There was a problem with removing snapshot ' + snapshot['DBSnapshotIdentifier'])
                print(e)
            else:
                print('Snapshot ' + snapshot['DBSnapshotIdentifier'] + ' has been deleted.')