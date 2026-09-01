from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect
from .forms import ContactForm

def contact_view(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            full_message = f"Від: {name} <{email}>\n\nПовідомлення:\n{message}"

            try:
                send_mail(
                    subject=subject,
                    message=full_message,
                    from_email=email,
                    recipient_list=['admin@greenstore.com'],
                    fail_silently=False,
                )
                messages.success(request, "Ваше повідомлення успішно відправлено!")
                return redirect('main:contact')
            except Exception as e:
                messages.error(request, f"Помилка при відправленні: {e}")
    else:
        form = ContactForm()

    context = {
        'title': 'Зворотний зв\'язок',
        'form': form,
        'categories': categories,
    }
    return render(request, 'main/contact.html', context)