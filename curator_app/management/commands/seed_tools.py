"""
Management command to seed Glintly with 45 curated AI tools.
Run with: py manage.py seed_tools
Run with --clear to wipe existing tools first: py manage.py seed_tools --clear
"""

from django.core.management.base import BaseCommand
from curator_app.models import AiTool


CURATED_TOOLS = [
    # ── NLP ──────────────────────────────────────────────────────────────────
    {
        'name': 'ChatGPT',
        'description': 'OpenAI\'s flagship conversational AI that can write, code, analyze data, answer questions, and assist with virtually any text-based task.',
        'link': 'https://chat.openai.com',
        'category': 'nlp',
        'is_featured': True,
        'is_popular': True,
    },
    {
        'name': 'Claude',
        'description': 'Anthropic\'s safety-focused AI assistant with a 200K context window — excellent for long documents, nuanced reasoning, and thoughtful writing.',
        'link': 'https://claude.ai',
        'category': 'nlp',
        'is_featured': True,
        'is_popular': True,
    },
    {
        'name': 'Gemini',
        'description': 'Google\'s multimodal AI that understands text, images, audio, and code — deeply integrated with Google Workspace and Search.',
        'link': 'https://gemini.google.com',
        'category': 'nlp',
        'is_featured': True,
        'is_popular': True,
    },
    {
        'name': 'Perplexity AI',
        'description': 'An AI-powered search engine that gives direct, cited answers instead of a list of links — ideal for research and quick fact-finding.',
        'link': 'https://perplexity.ai',
        'category': 'nlp',
        'is_featured': False,
        'is_popular': True,
    },
    {
        'name': 'Hugging Face',
        'description': 'The GitHub of AI — an open-source platform hosting thousands of pre-trained models, datasets, and Spaces for demos.',
        'link': 'https://huggingface.co',
        'category': 'nlp',
        'is_featured': True,
        'is_popular': True,
    },
    {
        'name': 'Mistral AI',
        'description': 'A European AI lab producing high-performance open-weight language models known for efficiency and strong reasoning at lower costs.',
        'link': 'https://mistral.ai',
        'category': 'nlp',
        'is_featured': False,
        'is_popular': False,
    },
    {
        'name': 'Cohere',
        'description': 'Enterprise NLP platform offering text generation, embeddings, and search APIs optimized for business applications.',
        'link': 'https://cohere.com',
        'category': 'nlp',
        'is_featured': False,
        'is_popular': False,
    },
    {
        'name': 'Grammarly',
        'description': 'AI writing assistant that checks grammar, style, tone, and clarity — now with generative AI features for drafting and rewriting.',
        'link': 'https://grammarly.com',
        'category': 'nlp',
        'is_featured': False,
        'is_popular': True,
    },
    {
        'name': 'Jasper AI',
        'description': 'Marketing-focused AI writing platform that generates blog posts, ads, social copy, and brand content at scale.',
        'link': 'https://jasper.ai',
        'category': 'nlp',
        'is_featured': False,
        'is_popular': False,
    },
    {
        'name': 'Notion AI',
        'description': 'Built into Notion, this AI assistant can summarize notes, draft documents, generate action items, and answer questions about your workspace.',
        'link': 'https://notion.so/product/ai',
        'category': 'nlp',
        'is_featured': False,
        'is_popular': True,
    },

    # ── CODE ─────────────────────────────────────────────────────────────────
    {
        'name': 'GitHub Copilot',
        'description': 'AI pair programmer built into VS Code and GitHub that suggests code completions, functions, and entire blocks based on context.',
        'link': 'https://github.com/features/copilot',
        'category': 'code',
        'is_featured': True,
        'is_popular': True,
    },
    {
        'name': 'Cursor',
        'description': 'AI-first code editor built on VS Code that can understand, write, and refactor entire codebases through natural language instructions.',
        'link': 'https://cursor.sh',
        'category': 'code',
        'is_featured': True,
        'is_popular': True,
    },
    {
        'name': 'Claude Code',
        'description': 'Anthropic\'s agentic coding tool that operates in your terminal — capable of editing files, running tests, and building entire features autonomously.',
        'link': 'https://claude.ai/code',
        'category': 'code',
        'is_featured': True,
        'is_popular': False,
    },
    {
        'name': 'Replit',
        'description': 'Browser-based IDE with an AI agent (Ghostwriter) that can build, run, debug, and deploy apps from natural language descriptions.',
        'link': 'https://replit.com',
        'category': 'code',
        'is_featured': False,
        'is_popular': True,
    },
    {
        'name': 'Tabnine',
        'description': 'AI code completion tool that learns your team\'s patterns and coding style, offering private, on-premise deployment for enterprise teams.',
        'link': 'https://tabnine.com',
        'category': 'code',
        'is_featured': False,
        'is_popular': False,
    },
    {
        'name': 'Bolt.new',
        'description': 'AI-powered full-stack web app builder by StackBlitz — describe what you want and it generates, runs, and deploys complete web apps instantly.',
        'link': 'https://bolt.new',
        'category': 'code',
        'is_featured': True,
        'is_popular': True,
    },
    {
        'name': 'v0 by Vercel',
        'description': 'Generates production-ready React UI components from text prompts or screenshots, using shadcn/ui and Tailwind CSS.',
        'link': 'https://v0.dev',
        'category': 'code',
        'is_featured': False,
        'is_popular': True,
    },
    {
        'name': 'Windsurf',
        'description': 'Codeium\'s agentic IDE with a "Flow" system that keeps AI context across your entire codebase for more coherent multi-file edits.',
        'link': 'https://codeium.com/windsurf',
        'category': 'code',
        'is_featured': False,
        'is_popular': False,
    },

    # ── IMAGE ─────────────────────────────────────────────────────────────────
    {
        'name': 'Midjourney',
        'description': 'The industry-leading AI image generator known for its stunning artistic quality — operates through Discord with a distinctive aesthetic.',
        'link': 'https://midjourney.com',
        'category': 'image',
        'is_featured': True,
        'is_popular': True,
    },
    {
        'name': 'DALL-E 3',
        'description': 'OpenAI\'s image generation model integrated into ChatGPT, capable of generating highly detailed images from complex text prompts.',
        'link': 'https://openai.com/dall-e-3',
        'category': 'image',
        'is_featured': True,
        'is_popular': True,
    },
    {
        'name': 'Stable Diffusion',
        'description': 'Open-source image generation model that can run locally on your own hardware, offering full control and unlimited generation.',
        'link': 'https://stability.ai',
        'category': 'image',
        'is_featured': False,
        'is_popular': True,
    },
    {
        'name': 'Adobe Firefly',
        'description': 'Adobe\'s family of AI models for image generation, style transfer, and generative fill — designed for commercial-safe creative work.',
        'link': 'https://firefly.adobe.com',
        'category': 'image',
        'is_featured': False,
        'is_popular': True,
    },
    {
        'name': 'Ideogram',
        'description': 'AI image generator that excels at embedding legible text inside images — a major weakness of most other generators.',
        'link': 'https://ideogram.ai',
        'category': 'image',
        'is_featured': False,
        'is_popular': False,
    },
    {
        'name': 'Canva AI',
        'description': 'Design platform with integrated AI tools for image generation, background removal, text-to-image, and one-click design creation.',
        'link': 'https://canva.com/ai-image-generator',
        'category': 'image',
        'is_featured': False,
        'is_popular': True,
    },
    {
        'name': 'Flux',
        'description': 'Black Forest Labs\' state-of-the-art open image generation model — praised for photorealism and fine detail, widely adopted in 2024-2025.',
        'link': 'https://blackforestlabs.ai',
        'category': 'image',
        'is_featured': True,
        'is_popular': False,
    },

    # ── MACHINE LEARNING ──────────────────────────────────────────────────────
    {
        'name': 'Hugging Face Transformers',
        'description': 'The definitive open-source library for state-of-the-art NLP models — load, fine-tune, and deploy thousands of pre-trained transformers in Python.',
        'link': 'https://huggingface.co/docs/transformers',
        'category': 'machine_learning',
        'is_featured': True,
        'is_popular': True,
    },
    {
        'name': 'LangChain',
        'description': 'Framework for building LLM-powered applications — chains together prompts, memory, tools, and agents for complex AI workflows.',
        'link': 'https://langchain.com',
        'category': 'machine_learning',
        'is_featured': True,
        'is_popular': True,
    },
    {
        'name': 'TensorFlow',
        'description': 'Google\'s open-source machine learning framework used to build and train neural networks for production at massive scale.',
        'link': 'https://tensorflow.org',
        'category': 'machine_learning',
        'is_featured': False,
        'is_popular': True,
    },
    {
        'name': 'PyTorch',
        'description': 'Facebook\'s flexible deep learning framework favored by researchers for its dynamic computation graphs and Python-first approach.',
        'link': 'https://pytorch.org',
        'category': 'machine_learning',
        'is_featured': False,
        'is_popular': True,
    },
    {
        'name': 'Weights & Biases',
        'description': 'MLOps platform for experiment tracking, model versioning, dataset management, and hyperparameter optimization.',
        'link': 'https://wandb.ai',
        'category': 'machine_learning',
        'is_featured': False,
        'is_popular': False,
    },
    {
        'name': 'Ollama',
        'description': 'Run powerful open-source LLMs like Llama 3, Mistral, and Gemma locally on your machine with a single terminal command.',
        'link': 'https://ollama.ai',
        'category': 'machine_learning',
        'is_featured': True,
        'is_popular': True,
    },
    {
        'name': 'LlamaIndex',
        'description': 'Data framework for connecting LLMs with private data sources — the backbone of most RAG (Retrieval Augmented Generation) pipelines.',
        'link': 'https://llamaindex.ai',
        'category': 'machine_learning',
        'is_featured': False,
        'is_popular': False,
    },
    {
        'name': 'Vertex AI',
        'description': 'Google Cloud\'s unified ML platform for building, deploying, and scaling models — includes access to Gemini and hundreds of foundation models.',
        'link': 'https://cloud.google.com/vertex-ai',
        'category': 'machine_learning',
        'is_featured': False,
        'is_popular': False,
    },

    # ── VISION ────────────────────────────────────────────────────────────────
    {
        'name': 'Roboflow',
        'description': 'End-to-end computer vision platform for annotating datasets, training object detection models, and deploying vision AI to production.',
        'link': 'https://roboflow.com',
        'category': 'vision',
        'is_featured': False,
        'is_popular': False,
    },
    {
        'name': 'Google Vision AI',
        'description': 'Google Cloud\'s pre-trained vision APIs for label detection, OCR, face detection, landmark recognition, and content moderation.',
        'link': 'https://cloud.google.com/vision',
        'category': 'vision',
        'is_featured': False,
        'is_popular': False,
    },
    {
        'name': 'Luma AI',
        'description': 'Creates stunning 3D scenes and videos from images using Neural Radiance Fields (NeRF) — also offers the Dream Machine video generator.',
        'link': 'https://lumalabs.ai',
        'category': 'vision',
        'is_featured': True,
        'is_popular': True,
    },
    {
        'name': 'Runway ML',
        'description': 'Creative AI studio for video generation, editing, and VFX — used by filmmakers and studios for AI-powered video production.',
        'link': 'https://runwayml.com',
        'category': 'vision',
        'is_featured': True,
        'is_popular': True,
    },
    {
        'name': 'Sora',
        'description': 'OpenAI\'s video generation model that creates realistic, high-quality video from text prompts — available to ChatGPT Pro subscribers.',
        'link': 'https://openai.com/sora',
        'category': 'vision',
        'is_featured': True,
        'is_popular': True,
    },

    # ── AUDIO ─────────────────────────────────────────────────────────────────
    {
        'name': 'ElevenLabs',
        'description': 'The leading AI voice synthesis platform — clones voices, creates custom AI narrators, and generates hyper-realistic speech in 30+ languages.',
        'link': 'https://elevenlabs.io',
        'category': 'audio',
        'is_featured': True,
        'is_popular': True,
    },
    {
        'name': 'Whisper',
        'description': 'OpenAI\'s open-source speech recognition model that transcribes audio in 100 languages with impressive accuracy, even in noisy environments.',
        'link': 'https://openai.com/research/whisper',
        'category': 'audio',
        'is_featured': False,
        'is_popular': True,
    },
    {
        'name': 'Suno AI',
        'description': 'Generates full songs — lyrics, vocals, and instrumentation — from a text prompt. Remarkably polished output across many genres.',
        'link': 'https://suno.ai',
        'category': 'audio',
        'is_featured': True,
        'is_popular': True,
    },
    {
        'name': 'Udio',
        'description': 'AI music generation platform that creates studio-quality songs from text descriptions, with fine-grained control over style and mood.',
        'link': 'https://udio.com',
        'category': 'audio',
        'is_featured': False,
        'is_popular': False,
    },
    {
        'name': 'Adobe Podcast',
        'description': 'AI-powered audio tools including Enhance Speech, which removes background noise and room echo from any recording in seconds.',
        'link': 'https://podcast.adobe.com',
        'category': 'audio',
        'is_featured': False,
        'is_popular': False,
    },
    {
        'name': 'Descript',
        'description': 'Edit audio and video by editing text — AI-powered overdub, filler word removal, and studio sound for podcasters and video creators.',
        'link': 'https://descript.com',
        'category': 'audio',
        'is_featured': False,
        'is_popular': True,
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with 45 curated AI tools. Use --clear to reset first.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing tools before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            count = AiTool.objects.count()
            AiTool.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Cleared {count} existing tools.'))

        created = 0
        updated = 0

        for tool_data in CURATED_TOOLS:
            obj, was_created = AiTool.objects.update_or_create(
                name=tool_data['name'],
                defaults={
                    'description':  tool_data['description'],
                    'link':          tool_data['link'],
                    'category':     tool_data['category'],
                    'is_featured':  tool_data['is_featured'],
                    'is_popular':   tool_data['is_popular'],
                }
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Done! {created} tools created, {updated} tools updated.\n'
                f'  Total tools in database: {AiTool.objects.count()}\n'
            )
        )