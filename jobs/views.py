from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Job, Proposal, Category
from .serializers import JobSerializer, ProposalSerializer, CategorySerializer
from django.shortcuts import get_object_or_404

# Create your views here.

class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "client"
    
    
class IsFreelancer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "freelancer"




class CategoryListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class JobListCreateView(APIView):
    def get(self, request):
        jobs = Job.objects.all().order_by('-created_at')
        serializer = JobSerializer(jobs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if not request.user.is_authenticated or request.user.role != 'client':
            return Response({'detail': 'Only clients can post jobs'}, status=status.HTTP_403_FORBIDDEN)

        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class JobDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Job, pk=pk)

    def get(self, request, pk):
        job = self.get_object(pk)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        job = self.get_object(pk)
        if request.user != job.client:
            return Response({'detail': 'You are not allowed to edit this job'}, status=status.HTTP_403_FORBIDDEN)

        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        job = self.get_object(pk)
        if request.user != job.client:
            return Response({'detail': 'You are not allowed to delete this job'}, status=status.HTTP_403_FORBIDDEN)

        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






class ProposalListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        proposals = Proposal.objects.all().order_by('-created_at')
        serializer = ProposalSerializer(proposals, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != 'freelancer':
            return Response({'detail': 'Only freelancers can send proposals'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProposalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(freelancer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# freelancers to see their propsals
class MyProposalsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'freelancer':
            return Response({'detail': 'Only freelancers can view this'}, status=status.HTTP_403_FORBIDDEN)

        proposals = Proposal.objects.filter(freelancer=request.user).order_by('-created_at')
        serializer = ProposalSerializer(proposals, many=True)
        return Response(serializer.data)


# Client to see freelancers proposals 
class JobProposalsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)

        if request.user != job.client:
            return Response({'detail': 'Only the job owner can view proposals'}, status=status.HTTP_403_FORBIDDEN)

        proposals = Proposal.objects.filter(job=job).order_by('-created_at')
        serializer = ProposalSerializer(proposals, many=True)
        return Response(serializer.data)

# Clients all POsted Jobs
class MyJobsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'client':
            return Response({'detail': 'Only clients can view this'}, status=status.HTTP_403_FORBIDDEN)

        jobs = Job.objects.filter(client=request.user).order_by('-created_at')
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


class FreelancerDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'freelancer':
            return Response({'detail': 'Only freelancers can access this'}, status=status.HTTP_403_FORBIDDEN)

        proposals = Proposal.objects.filter(freelancer=request.user).select_related('job')
        jobs = [p.job for p in proposals]
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    
    
    
    
    
# Accept / Reject Proposal API
class ProposalStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, proposal_id):
        proposal = get_object_or_404(Proposal, id=proposal_id)

        if request.user != proposal.job.client:
            return Response({'detail': 'Only the job owner can accept/reject proposals'},
                            status=status.HTTP_403_FORBIDDEN)

        action = request.data.get('action')

        if action not in ['accept', 'reject']:
            return Response({'detail': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        proposal.status = 'accepted' if action == 'accept' else 'rejected'
        proposal.save()

        return Response({'status': proposal.status, 'message': f"Proposal {proposal.status} successfully!"})





# class MessageListCreateView(APIView):
#     # permission_classes = [IsAuthenticated]

#     def get(self, request, job_id):
#         job = Job.objects.get(pk=job_id)

#         # Ensure user is involved in the job
#         if request.user != job.client and not job.proposals.filter(freelancer=request.user).exists():
#             return Response({'detail': 'You are not part of this job.'}, status=status.HTTP_403_FORBIDDEN)

#         messages = Message.objects.filter(job=job).order_by('timestamp')
#         serializer = MessageSerializer(messages, many=True)
#         return Response(serializer.data)

#     def post(self, request, job_id):
#         job = Job.objects.get(pk=job_id)

#         # Same authorization check
#         if request.user != job.client and not job.proposals.filter(freelancer=request.user).exists():
#             return Response({'detail': 'You are not part of this job.'}, status=status.HTTP_403_FORBIDDEN)

#         data = request.data.copy()
#         data['sender'] = request.user.id
#         data['job'] = job.id

#         serializer = MessageSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save(sender=request.user)
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)