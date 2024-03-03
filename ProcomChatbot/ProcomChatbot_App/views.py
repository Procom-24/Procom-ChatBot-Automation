from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from rest_framework.decorators import api_view, schema
from rest_framework.response import Response
from rest_framework import status

from .forms import UserLoginForm, UserRegistrationForm
import os
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
from django.http import StreamingHttpResponse
from django.utils import timezone
import time


# Setting OpenAI variables
OPEN_AI_API_KEY = "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"
embedding_model = "text-embedding-ada-002"
openai_client = OpenAI(api_key=OPEN_AI_API_KEY)

# This is OpenAI embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPEN_AI_API_KEY,
    model_name=embedding_model,
)


def chatbot(request):
    try:
        chroma_client = chromadb.Client()
        chroma_client = chromadb.PersistentClient(path="media/Procom/database/")
        collection = chroma_client.get_collection(
            name="Procom_Competitions", embedding_function=openai_ef
        )
    except:
        return redirect("ProcomChatbot_App:error_page")
    return render(request, "ProcomChatbot_App/chatbot.html")


def page_not_found_404(request, exception, message="No page found"):
    return render(
        request,
        "ProcomChatbot_App/page_not_found_404.html",
        {"message": message},
        status=404,
    )


def error_page(request):
    message = "Server Error"
    return render(
        request,
        "ProcomChatbot_App/error_page.html",
        {"message": message},
    )


# Account Related Views
def user_login(request):
    if request.method == "POST":
        login_form = UserLoginForm(request, request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Attempt to sign user in
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("ProcomChatbot_App:chatbot")
            else:
                return render(
                    request,
                    "ProcomChatbot_App/login.html",
                    {
                        "login_form": login_form,
                    },
                )
        else:
            return render(
                request,
                "ProcomChatbot_App/login.html",
                {
                    "login_form": login_form,
                },
            )
    else:
        return render(
            request,
            "ProcomChatbot_App/login.html",
            {
                "login_form": UserLoginForm(),
            },
        )


def user_logout(request):
    logout(request)
    return redirect("ProcomChatbot_App:user_login")


def user_register(request):
    if request.method == "POST":
        signup_form = UserRegistrationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            return redirect("ProcomChatbot_App:chatbot")
        else:
            return render(
                request,
                "ProcomChatbot_App/register.html",
                {"register_form": UserRegistrationForm(request.POST)},
            )
    return render(
        request,
        "ProcomChatbot_App/register.html",
        {
            "register_form": UserRegistrationForm(),
        },
    )


# API
@api_view(["POST"])
def send_message(request):
    data = {"response": None, "status": 403, "error": "Someting went wrong."}

    # Create a JsonResponse object with the JSON data
    if request.method == "POST":
        received_data = request.data
        user_query = received_data["user_query"]
        try:
            chroma_client = chromadb.Client()
            chroma_client = chromadb.PersistentClient(path="media/Procom/database/")
            collection = chroma_client.get_or_create_collection(
                name="Procom_Competitions", embedding_function=openai_ef
            )

            # embedded_query = get_embedding(user_query, model=embedding_model)
            # result = collection.query(
            #     query_embeddings=embedded_query,
            #     n_results=3,
            # )
            # query_set = result["documents"][0]
            # query_respond = "\n".join(str(item) for item in query_set)
            # bot_response = ask_openai(user_query, query_respond)

            # data["response"] = bot_response
            t = collection.query(query_texts=user_query)
            data["response"] = t["documents"][0][0]
            data["status"] = 200
            data["error"] = None

        except:
            pass  # Already handled

    return Response(data)


# OPEN_AI_API_KEY = "GONNA ADD THINSG LATER"
# embedding_model = "text-embedding-ada-002"
# client = OpenAI(api_key=OPEN_AI_API_KEY)
# openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#     api_key=OPEN_AI_API_KEY,
#     model_name=embedding_model,
# )


# def ask_openai(user_query, query_respond):
#     system_message = f"""
#     Your task is to answer user questions based solely
#     on the provided information.You can not answer the
#     user query from your knowledge. If the user's query is
#     within the scope of the provided information, you
#     will provide an answer. However, if the query is not
#     relevant to the information provided, you will respond
#     with: "Your query seems like it's out of my knowledge."
#     Below is the available information:
#     INFORMATION
#     ####
#     {query_respond}
#     ####
#     """
#     messages = [
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": user_query},
#     ]

#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo", messages=messages, temperature=0
#     )

#     response_message = response.choices[0].message.content
#     return response_message


# def get_embedding(text, model=embedding_model):
#     text = text.replace("\n", " ")
#     return client.embeddings.create(input=[text], model=model).data[0].embedding
