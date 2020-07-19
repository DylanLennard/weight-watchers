import weight_watchers


def lambda_handler(event, context):
    """Call the script"""
    weight_watchers.run()
