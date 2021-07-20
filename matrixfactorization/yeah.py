from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import Http404
from client.models import Music, Review,Rating
from django.contrib import messages

from django.db.models import Case, When
from .recommendation import Myrecommend
import numpy as np
import pandas as pd


# for recommendation
def recommend1(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    review_df = pd.DataFrame(list(Rating.objects.all().values()))
    rename_review_df = review_df.rename(columns={"song_id":"music_id"})
    music_df = pd.DataFrame(list(Music.objects.all().values()))
    music = Music.objects.all().values()
    print(music)
    print("==========================================")
    hack = pd.DataFrame(music)
    print(hack)
    # print(review_df)
    # print(music_df)
    # print("-----------------------------------")
    # print(rename_review_df)
    dataset =  pd.merge(review_df, rename_review_df, on = "user_id")
    # print("------------------------------------------Full Dataset----------------------------------------")
    # print(dataset)
    # group = dataset.groupby('user_id')
    # print("Group By Title: ", group)

    # newdf = df[(df.user_id == request.user.id)]
    # print("New Datafrme:", newdf)
    # context = {
    #     "data": newdf
    # }
    # print("Context: ", context)
    # song_id = df.song_id.unique().shape[0]
    # print("Music ID: ", song_id)
    # current_user_id = request.user.id
    # match_user_id = df.user_id
    # print("Matched User Id", current_user_id)
    # print("Current user id: ", current_user_id)

    # if current_user_id == match_user_id:
    #     print("Success!!")
    # else:
    #     print("Fail !!")   
    return render(request, 'recommend.html', {"context": dataset.to_html()})


    

    # print("Current user id: ", current_user_id)
    # prediction_matrix, Ymean = Myrecommend()
    # my_predictions = prediction_matrix[:, current_user_id - 1] + Ymean.flatten()
    # pred_idxs_sorted = np.argsort(my_predictions)
    # pred_idxs_sorted[:] = pred_idxs_sorted[::-1]
    # pred_idxs_sorted = pred_idxs_sorted + 1
    # print(pred_idxs_sorted)
    # preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pred_idxs_sorted)])
    # music_list = list(Product.objects.filter(id__in=pred_idxs_sorted, ).order_by(preserved)[:10])
    # return render(request, 'recommend.html', {'music_list': music_list})
