from django.shortcuts import render, redirect, get_object_or_404


def view_retreat(request):
    """ A view that returns the retreat that a user has customised
    and designed after their own preferences """

    return render(request, 'retreat/retreat.html')


def add_to_retreat(request, item_id, item_type):
    """ A view that allows users to add items to their retreat,
    regardless of which class they belong to """

    item = get_object_or_404(item_type.capitalize(), pk=item_id)

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    retreat = request.session.get('retreat', {})

    if request.user.is_authenticated:
        if item_id in list(retreat.keys()):
            retreat[item_id] += quantity
        else:
            retreat[item_id] = quantity

        request.session['retreat'] = retreat
        print(request.session['retreat'])
        return redirect(redirect_url, {'item': item})
