from django.urls import path
from .views import JobListCreateView, JobDetailView, ProposalListCreateView, ProposalStatusUpdateView

urlpatterns = [
    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('proposals/', ProposalListCreateView.as_view(), name='proposal-list-create'),
    path('proposals/<int:proposal_id>/status/', ProposalStatusUpdateView.as_view(), name='proposal-status-update'),

]


from .views import (
    MyProposalsView,
    JobProposalsView,
    MyJobsView,
    FreelancerDashboardView,
    CategoryListCreateView,
)

urlpatterns += [
    path('my-proposals/', MyProposalsView.as_view(), name='my-proposals'),
    path('jobs/<int:job_id>/proposals/', JobProposalsView.as_view(), name='job-proposals'),
    path('my-jobs/', MyJobsView.as_view(), name='my-jobs'),
    path('freelancer-dashboard/', FreelancerDashboardView.as_view(), name='freelancer-dashboard'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
]