import math, socket
from django.shortcuts import render
from .forms import InputForm

def calculator_view(request):
    host = socket.gethostname()  # helpful to prove load balancing
    result = None
    error = None
    notes = []

    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            c = form.cleaned_data['c']

            # Extra safety (division by zero)
            if a == 0:
                error = "Value A cannot be zero because we may divide by A."
            elif c < 0:
                error = "Value C cannot be negative."
            else:
                if a < 1:
                    notes.append("A is less than 1 — input may be too small.")
                if b == 0:
                    notes.append("B is 0 — it will not affect the result.")

                c3 = c ** 3
                if c3 > 1000:
                    base = math.sqrt(c3) * 10
                else:
                    base = math.sqrt(c3) / a

                final = base + b

                # Stitch notes into the result text
                if notes:
                    result = f"{final:.6f} (Notes: " + " | ".join(notes) + ")"
                else:
                    result = f"{final:.6f}"
        else:
            error = "Please enter valid numeric values for A, B, and C."
    else:
        form = InputForm()

    return render(request, 'calculator/result.html', {
        'form': form,
        'result': result,
        'error': error,
        'host': host,
    })
