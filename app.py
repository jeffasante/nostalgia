from flask import Flask, render_template, request
from livereload import Server
# from recsys import getRecommendations #show_popular
# from fetch_img import engine as engine
from bing_fetch import bingEngine


app = Flask(__name__)





import pickle, re

save_dir = 'resources/weights/cbf_weights.p'
title_imglink_dir = 'resources/misc/title_imglink.p'


handler = pickle.load( open(save_dir, 'rb') )
title_link = pickle.load( open(title_imglink_dir, 'rb') )

def dumpPickle(f, f_dir):
    # if a == 0:
    pickle.dump(f, open(f_dir, 'wb'))
    # if a == 1:
    #     pickle.load( open(title_imglink_dir, 'rb') )

def loadAllPickle(filename):
    with open(filename, "rb") as f:
        while True:
            try:
                return pickle.load(f)
            except EOFError:
                break


# handler = loadAllPickle(save_dir)
# title_link = loadAllPickle(title_imglink_dir)

# print(handler)


movies_df = handler['movies_df']
indices = handler['indices']
cosine_sim = handler['cosine_sim2']
# print(indices)
title_lookup = list({v: k for k, v in indices.items()}.values())
# print(title_lookup)


# make prediction
def getRecommendations(title, movies_df=movies_df,
         indices=indices, cosine_sim=cosine_sim):

    # get index of the movie that match `title`
    idx = indices[title]

    # get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # print(sim_scores)

    # sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # get the scores of the top 10 most similar movies
    sim_scores = sim_scores[1: 11] # a most similar movie is itself, ignore the first index

    # getvthe movie indices
    movie_indices = [i[0] for i in sim_scores]

    # return the top 10 most similar movie_indices
    return movies_df['title'].iloc[movie_indices].tolist()




# get image from bingEngine
def engine(d):
    return {data[i]: bingEngine(data[i] + ' movie') for i in range(6)}


import string, unicodedata
# all_letters = string.ascii_letters + " .,;'-"
# def unicodeToAscii(s):
#     return ''.join(
#         c for c in unicodedata.normalize('NFD', s)
#         if unicodedata.category(c) != 'Mn'
#         and c in all_letters
#     )
all_letters = string.ascii_letters + " .,;'-"
def unicodeToAscii(s):
    # s = ''.join(s.split(' '))
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
        and c in all_letters
    )


def trimText(s):
    return re.sub(r'[^\w]', '', s)



# import threading
# import multiprocessing

# cached = {}
# img_links_cache = {}
img_links_cache = title_link if title_link != {} else {}
print(img_links_cache)
# print('\n', title_lookup, '\n')
# @app.context_processor
@app.route('/', methods=['GET', 'POST'])
def my_form_post():
    

    
    if request.method == "POST":

        
        text = unicodeToAscii(request.form.get('text').lower()).strip()
        # text = trimText(unicodeToAscii(request.form.get('text').lower())).replace(' ', '')
        user_query = [v for v in title_lookup if text in v]
        
        # flag = True
        print(text)
        
        try:
            
            print('text in ')

            if text not in img_links_cache:
                
                # if link isnt saved, fetch from net and save

                data = getRecommendations(text)
                print(data)
                print(data[0])
                print()

                # cached[text] = {}
                # cached[text] = data

                while True:
                    for t in data[:6]:
                        if t not in img_links_cache:
                            img_link = bingEngine(unicodeToAscii(t))
                            img_links_cache[t] = img_link
                        else:
                            continue
                    
                    dumpPickle(img_links_cache, title_imglink_dir)
                    print('saved to ' + title_imglink_dir)
                    print()
                    break

                # image_url = {data[i]: bingEngine(unicodeToAscii(data[i])) for i in range(6)}
                # cached[text]['img_url'] = image_url

                # print(cached[text]['img_url'])
                return render_template('index.htm', data=data, flag=True,
                      img=img_links_cache, user_text=text)
                
            else:
                # data = cached[text]
                # a quick way to query the link instead of always scraping
                print('\n seems we are stored here')
                data = getRecommendations(text)

                image_url = {}

                while True:
                    for t in data[:6]:
                        if t not in img_links_cache: # if not found, scrape

                            img_link = bingEngine(unicodeToAscii(t))
                            img_links_cache[t] = img_link
                            image_url[t] = img_links_cache[t]

                        else: # if found set it to a dictionary for flask
                            image_url[t] = img_links_cache[t]
                            continue
                    
                    dumpPickle(img_links_cache, title_imglink_dir)
                    print('saved to ' + title_imglink_dir) 
                    print()
                    break
                # image_url = {t: img_links_cache[t] if t in img_links_cache else bingEngine(unicodeToAscii(t)) for t in data[:6] }

                # image_url = [img_links_cache[t] if t in img_links_cache else bingEngine(unicodeToAscii(t)) for t in data[:6] ]
                # image_url = image_url[text]['img_url']
                # image_url = {data[i]: bingEngine(unicodeToAscii(data[i])) for i in range(6)}
                return render_template('index.htm', data=data, flag=True,
                      img=image_url, user_text=text)

            # image_url = {data[i]: bingEngine(unicodeToAscii(data[i])) for i in range(6)}
            
            # print()
            # print(image_url)
            print()
            # return render_template('index.htm', data=data, flag=True,
            #           img=image_url, user_text=text)
            # return render_template('index.htm',
            #      data=data, flag=True, user_text=text, bingFunc=bingEngine)

        except:

            print("Something else went wrong")
            error = 'result not found!'
            print(user_query)   
            return render_template('index.htm', data=[], 
                error=error, user_query=user_query, flag=False,
                title_list=title_lookup)
        
    # return render_template('index.htm', data=[], 
    # title_list=title_lookup
    # )
    return render_template('index.htm', data=[])
    




if __name__ == '__main__':
   
    app.debug = True
    server = Server(app.wsgi_app)
    server.serve()
    


