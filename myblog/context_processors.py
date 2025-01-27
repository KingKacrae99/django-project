def Notifications(request):
    if request.user.is_authenticated:
        unread_nofitications = request.user.notifications.filter(is_read=False)
        notifications = request.user.notifications.all().order_by('-timestamp')[:10]
        total_unread = unread_nofitications.count()

    else:
        notifications = []
        total_unread = 0

    context={
        'total_unread': total_unread,
        'notifications': notifications,
    }
    return context