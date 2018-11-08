from datetime import datetime, timedelta


def get_scraped_date(request):
    try:
        days = int(request.args.get('days_old', 0))
        return (datetime.now() - timedelta(days=days)
                ).strftime("%Y-%m-%d")
    except TypeError as e:
        return datetime.now().strftime("%Y-%m-%d")
