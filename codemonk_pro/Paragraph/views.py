from rest_framework import generics, permissions
from .models import Paragraph, WordFrequency
from .serializers import ParagraphSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import process_paragraphs

class ParagraphCreateView(generics.CreateAPIView):
    serializer_class = ParagraphSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        paragraphs = request.data['text'].split('\n\n')
        created = []
        for p in paragraphs:
            para = Paragraph.objects.create(user=request.user, text=p.strip())
            created.append(para)
        # Async frequency counting
        process_paragraphs.delay([para.id for para in created], request.user.id)
        return Response(ParagraphSerializer(created, many=True).data)

class ParagraphWordSearchAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        word = request.query_params.get('word', '').lower()
        user = request.user
        paras = Paragraph.objects.filter(user=user)
        para_scores = [
            (para, para.text.lower().split().count(word))
            for para in paras if word in para.text.lower().split()
        ]
        para_scores = sorted(para_scores, key=lambda x: -x[1])[:10]
        return Response([
            {
                "paragraph_id": para.id,
                "text": para.text,
                "occurrences": score
            } for para, score in para_scores
        ])

