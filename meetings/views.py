from django.shortcuts import render
from rest_framework import viewsets
import requests
from .models import Transcript
from .serializers import TranscriptSerializer
from decouple import config
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .clients import FirefliesClient
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer ,TranscriptSummarySerializer , UploadAudioSerializer

class TranscriptViewSet(viewsets.ModelViewSet):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptSerializer



class TranscriptListView(APIView):
    def get(self, request):
        fireflies_client = FirefliesClient()
        try:
            # Fetch users from Fireflies using the GraphQL request
            users_data = fireflies_client.get_users()
            return Response(users_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TranscriptSummaryView(APIView):
    def post(self, request):
        # Validate the input using the serializer
        serializer = TranscriptSummarySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract the validated data
        transcript_id = serializer.validated_data.get('transcriptId')

        if transcript_id:
            return self.fetch_transcript_summary(transcript_id)
        else:
            return self.fetch_all_transcripts()

    def get(self, request):
        # Get transcript ID from query parameters
        transcript_id = request.query_params.get("transcriptId")

        if transcript_id:
            return self.fetch_transcript_summary(transcript_id)
        else:
            return self.fetch_all_transcripts()

    def fetch_transcript_summary(self, transcript_id):
        # Get API key and GraphQL URL from environment variables or settings
        api_key = config('FIREFLIES_API_KEY')
        url = config('FIREFLIES_BASE_URL')

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # GraphQL query for retrieving transcript summary
        data = {
            "query": """
            query Transcript($transcriptId: String!) {
                transcript(id: $transcriptId) {
                    summary {
                        keywords
                        action_items
                        outline
                        shorthand_bullet
                        overview
                        bullet_gist
                        gist
                        short_summary
                    }
                }
            }
            """,
            "variables": {"transcriptId": transcript_id}
        }

        try:
            # Make the POST request to Fireflies.ai GraphQL API
            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()

            if response.status_code == 200 and "errors" not in response_data:
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(response_data.get("errors", "Unknown error"), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def fetch_all_transcripts(self):
        # Get API key and GraphQL URL from environment variables or settings
        api_key = config('FIREFLIES_API_KEY')
        url = config('FIREFLIES_BASE_URL')

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Adjusted GraphQL query for retrieving all transcripts (without the unsupported 'created_at' field)
        data = {
            "query": """
            query {
                transcripts {
                    id
                    title
                    duration
                    summary {
                        short_summary
                        gist
                    }
                }
            }
            """
        }

        try:
            # Make the POST request to Fireflies.ai GraphQL API
            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()

            if response.status_code == 200 and "errors" not in response_data:
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(response_data.get("errors", "Unknown error"), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class UploadAudioView(APIView):
    def post(self, request):
        # Get API key and base URL from environment variables or settings
        api_key = config('FIREFLIES_API_KEY')
        url = config('FIREFLIES_BASE_URL')

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Define required input fields
        required_fields = ["webhook", "audio_url", "title"]
        input_data = {
            "webhook": request.data.get("webhook"),
            "url": request.data.get("audio_url"),
            "title": request.data.get("title"),
            "attendees": request.data.get("attendees", [])
        }

        # Check if any required field is missing
        missing_fields = [field for field in required_fields if not input_data.get(field)]
        if missing_fields:
            return Response(
                {"error": f"Missing required fields: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # GraphQL mutation for uploading audio
        data = {
            "query": """
            mutation($input: AudioUploadInput) {
                uploadAudio(input: $input) {
                    success
                    title
                    message
                }
            }
            """,
            "variables": {"input": input_data}
        }

        try:
            # Make the POST request to Fireflies.ai GraphQL API
            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()

            # Handle response and return result
            if response.status_code == 200 and "errors" not in response_data:
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(
                    response_data.get("errors", "Unknown error"),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer