from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, PDFUploadForm, CommentForm
from .models import PDFFile, ShareLink, Comment
from django.db.models import Q

# User Signup
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# User Login
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# User Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard with search and PDF list
@login_required
def dashboard(request):
    query = request.GET.get('q', '')
    if query:
        pdfs = PDFFile.objects.filter(owner=request.user, name__icontains=query)
    else:
        pdfs = PDFFile.objects.filter(owner=request.user)
    return render(request, 'dashboard.html', {'pdfs': pdfs, 'query': query})

# PDF Upload
@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.owner = request.user
            pdf.save()
            return redirect('dashboard')
    else:
        form = PDFUploadForm()
    return render(request, 'upload.html', {'form': form})

# PDF Detail + comments (for owner and authenticated users)
@login_required
def pdf_detail(request, pdf_id):
    pdf = get_object_or_404(PDFFile, id=pdf_id)
    if pdf.owner != request.user:
        return redirect('dashboard')  # unauthorized access

    comments = pdf.comments.order_by('created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.pdf = pdf
            comment.user = request.user
            comment.save()
            return redirect('pdf_detail', pdf_id=pdf.id)
    else:
        form = CommentForm()
    return render(request, 'pdf_detail.html', {'pdf': pdf, 'comments': comments, 'form': form})

# Generate share link
@login_required
def generate_share_link(request, pdf_id):
    pdf = get_object_or_404(PDFFile, id=pdf_id, owner=request.user)
    link, created = ShareLink.objects.get_or_create(pdf=pdf)
    share_url = request.build_absolute_uri(f'/shared/{link.uuid}/')
    return render(request, 'share_link.html', {'share_url': share_url, 'pdf': pdf})

# Access shared PDF by invited user (no login needed)
def shared_pdf_view(request, uuid):
    link = get_object_or_404(ShareLink, uuid=uuid)
    pdf = link.pdf
    comments = pdf.comments.order_by('created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.pdf = pdf
            # invited user, no Django User instance
            comment.user = None
            comment.save()
            return redirect('shared_pdf', uuid=uuid)
    else:
        form = CommentForm()
    return render(request, 'shared_pdf.html', {'pdf': pdf, 'comments': comments, 'form': form})
from django.shortcuts import render

# Create your views here.
