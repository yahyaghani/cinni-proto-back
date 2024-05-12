from openai import OpenAI
import json
import os 
import ast


from src.parser_helpers import extract_list_from_string

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



def no_context_request_more_context(keyword_list):
    prompt=f"""
    You are a shopping assistant, you have to help guide the user through their shopping journey, all you have are the possible things that may interest them in keyword_list:
    
    here are some examples of your thought process :-

    Example 1 User: {example_keyword_list_1}
    Answer: Ah that's certainly a stylish Coat, do you need me to search similar Shoes and Sunglasses with it or just a similar Coat for now?

    Example 2 User: {example_keyword_list_2}
    Answer: For your beach day, how about some trendy Sunglasses and a stylish Hat to go with your Swimwear? I can also find a new Beach Bag and Sandals if you're looking to update your beach attire.

    Example 3 User:  {example_keyword_list_3}
    Answer: Looking for another stunning Formal Dress for a wedding? I can suggest some elegant High Heels and a matching Clutch. Would you also like to see some Jewelry options or perhaps a Wrap to complete the look?

    New query :{keyword_list}
    Answer:
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            # model="gpt-4",

            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful Shopping Assistant, called Cinni AI, your goal is to converse with the user to delve into their shopping queries to ask leading questions that can help identify what style,color,size,occasion,materials they prefer. You utilise your previous history with the user to understand and shape their shopping journey.."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=500,
            n=1,
            temperature=0.50,  
        )
        # answer = response.choices[0].message['content'].strip()
        answer_json_string=(response.model_dump_json(indent=2))
        answer_dict = json.loads(answer_json_string)
        answer = answer_dict['choices'][0]['message']['content']

    except Exception as e:
        answer = "None"
        print(e)

    return answer








######
example_query_1='i need this one'
example_keyword_list_1=["Pants","Shoe","Outerwear","Sunglasses","Coat","Clothing"]
example_historical_context_1="None"

example_query_2='Looking for an outfit for a beach day'
example_keyword_list_2=["Swimwear", "Sandals", "Hat", "Beach Bag", "Sunglasses"]
example_historical_context_2="browsed swimwear and sandals"

example_query_3='Need a dress for a wedding'
example_keyword_list_3=["Formal Dress", "High Heels", "Clutch", "Jewelry", "Wrap"]
example_historical_context_3="Previously bought a formal dress last year"


# You are a shopping assistant, you have to identify and select the keywords to target based on a users query and historical context:


def basic_shopping_prompt(user_query,keyword_list,historical_context):
    prompt=f"""
    You are a shopping assistant, you have to identify and answer the users query with historical context to help them in their shopping journey:
    
    here are some examples of your thought process :-

    Example 1 query{example_query_1},{example_keyword_list_1},{example_historical_context_1}
    Answer: Ah that's certainly a stylish Coat, do you need me to search similar Shoes and Sunglasses with it or just a similar Coat for now?

    Example 2 query: {example_query_2}, {example_keyword_list_2}, {example_historical_context_2}
    Answer: For your beach day, how about some trendy Sunglasses and a stylish Hat to go with your Swimwear? I can also find a new Beach Bag and Sandals if you're looking to update your beach attire.

    Example 3 query: {example_query_3}, {example_keyword_list_3}, {example_historical_context_3}
    Answer: Looking for another stunning Formal Dress for a wedding? I can suggest some elegant High Heels and a matching Clutch. Would you also like to see some Jewelry options or perhaps a Wrap to complete the look?

    New query :{user_query},{keyword_list},{historical_context}
    Answer:
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            # model="gpt-4",

            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful Shopping Assistant, called Cinni AI, your goal is to converse with the user to delve into their shopping queries to ask leading questions that can help identify what style,color,size,occasion,materials they prefer. You utilise your previous history with the user to understand and shape their shopping journey.."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=500,
            n=1,
            temperature=0.15,  
        )
        # answer = response.choices[0].message['content'].strip()
        answer_json_string=(response.model_dump_json(indent=2))
        answer_dict = json.loads(answer_json_string)
        answer = answer_dict['choices'][0]['message']['content']

    except Exception as e:
        answer = "None"
        print(e)

    return answer


example_query_1='i need this one'
example_keyword_list_1=["Jeans","Clothing"]
example_historical_context_1="I was thinking about what to wear for an office party tonight "


# res=basic_shopping_prompt(example_query_1,example_keyword_list_1,example_historical_context_1)
# print(res)


#### provide answerable options based on the question

example_question="Ah, it seems like you're looking for a pair of jeans. That's a classic choice! Could you please provide me with some more information to help narrow down the options? What style of jeans are you looking for? Are you interested in a specific color or wash? And do you have a preferred size or fit in mind?"

def provide_answer_options(question):
    prompt=f"""
    You are a filtering assistant, you have to identify the question provided to you ,
    and return a python list that contains 3 options to answer the question:
    
    here are some examples of your thought process :-

    Example 1 query:"hmm bikini , what else do you need for your beach party?"
    Example 1 Answer : ['how about some sandals','a pair of sunglasses','maybe a Hat to prevent sunburns']

    Example 2 query:"Ah, I remember you mentioning that you were looking for an outfit for an office party. Have you considered pairing those jeans with a stylish blouse or a dressy top? It could give you a chic and sophisticated look for the party. Do you have any color preferences for the top?" 
    Example 2 Answer:['A nice blouse in a neutral color would be great', 'A dressy top in a bold color could make a statement', 'A printed top with some embellishments would add some flair']
    
    Example 3 query:{example_question}
    Example 3 Answer: ['Just Straight & Slim please', 'Bootcut', 'I need a jacket in military style to go with it']
 
    ## Query:{question}
    Answer: 
    
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            # model="gpt-4",

            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful Shopping Assistant, called Cinni AI."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=500,
            n=1,
            temperature=0.1,  
        )
        # answer = response.choices[0].message['content'].strip()
        answer_json_string=(response.model_dump_json(indent=2))
        answer_dict = json.loads(answer_json_string)
        answer = answer_dict['choices'][0]['message']['content']
    except Exception as e:
        print(e)
        answer = "None"
    return answer

# # provide_qqsuestion="Certainly! I'd be happy to help you find a new pair of glasses. Could you please provide me with more details about the style, color, and size you prefer? Additionally, do you have any specific occasion or material in mind?"
# provide_qqsuestion="Do you need just the Shirt or the shoes or should i pick out a whole attire for this event ?"

# filter_test=provide_answer_options(res)

# print(filter_test)

# # ###

filter_example_keyword_list_1=['Outerwear', 'Arm','Sleeve', 'Grey', 'Collar', 'Blazer', 'Beard', 'Formal wear', 'Hip','Suit', 'Denim', 'Dress shirt']
example_historical_context_1="I was thinking about what to wear for an office party tonight "

filter_example_keyword_list_2 = ['Blazer', 'Office partywear', 'Bikini','Sandals','costume','Denim', 'Dress shirt','Black', 'Suit', 'Dress', 'Formal shoes', 'Tie', 'Scarf', 'Dress coat', 'Mourning band']
example_historical_context_2 = "Last time I attended a service, I felt underdressed and want to ensure I'm appropriately solemn and respectful this time."

filter_example_keyword_list_3 = ['High Heels','Tuxedo','Dress shoes','Ties','T-shirt', 'Jeans', 'Sneakers', 'Cap', 'Sundress', 'Cargo shorts', 'Leggings', 'Jumper']
example_historical_context_3 = "Last party, my outfit was too formal and not suitable for playing games with the kids. This time, I want something more relaxed and fun to wear."

filter_example_keyword_list_4=['Leg','Eyewear', 'Sunglasses','Clothing']
example_historical_context_4='prom night tonight'


def identify_labels_to_crop(keyword_list,provided_historical_context):
    prompt=f"""
    You are a filtering assistant, you have to identify the items provided to you in the list based on the context of the historical context,
    and return a python list that only contains the words that are relevant articles of clothing. Try to keep only the most relevant ones:
    
    here are some examples :-

    Example 1 query:{filter_example_keyword_list_1},{example_historical_context_1}
    Example 1 Answer: ['Blazer','Denim', 'Dress shirt']

    Example 2 query:{filter_example_keyword_list_2},{example_historical_context_2}
    Example 2 Answer: ['Mourning band','Collar','Formal wear','Black,'Scarf']

    Example 3 query:{filter_example_keyword_list_3},{example_historical_context_3}
    Example 3 Answer: ['T-shirt', 'Jeans', 'Sneakers', 'Cap', 'Sundress', 'Cargo shorts']

    Example 4 query:{filter_example_keyword_list_4},{example_historical_context_4}
    Example 4 Answer: ['Leg', 'Eyewear','Clothing]


    ## Query:{keyword_list},{provided_historical_context}
    Answer :
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            # model="gpt-4",

            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful filtering Assistant, called Cinni AI."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=700,
            n=1,
            temperature=0.1,  
        )
        # answer = response.choices[0].message['content'].strip()
        answer_json_string=(response.model_dump_json(indent=2))
        answer_dict = json.loads(answer_json_string)
        answer = answer_dict['choices'][0]['message']['content']
        answer=extract_list_from_string(answer)


    except Exception as e:
        print(e)
        answer = "None"
    return answer



# filter_test=['tuxedo','cargo shorts', 'Sunglasses']
# historical_context='so you need jeans'
# rest=identify_labels_to_crop(filter_test,historical_context)
# print(rest)


###

def davinci_results_sentence(question):

    prompt = f""" You are a filtering assistant, you have to identify the question provided to you ,
    and return a python list that contains 3 options to answer the question:
    
    here are some examples of your thought process :-

    Example 1 query:"hmm bikini , what else do you need for your beach party?"
    Example 1 Answer : ['how about some sandals','a pair of sunglasses','maybe a Hat to prevent sunburns']

    Example 2 query:"Ah, I remember you mentioning that you were looking for an outfit for an office party. Have you considered pairing those jeans with a stylish blouse or a dressy top? It could give you a chic and sophisticated look for the party. Do you have any color preferences for the top?" 
    Example 2 Answer:['A nice blouse in a neutral color would be great', 'A dressy top in a bold color could make a statement', 'A printed top with some embellishments would add some flair']
    
    Example 3 query:{example_question}
    Example 3 Answer: ['Just Straight & Slim please', 'Bootcut', 'I need a jacket in military style to go with it']
 
    ## Query:{question}
    Answer: 


    """
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=350,
            n=1,
            stop=None,
            temperature=0.1,
        )
        # answer = response.choices[0].text.strip()
        # print(response)
        answer_json_string=(response.model_dump_json(indent=2))
        answer_dict = json.loads(answer_json_string)
        # print(answer_dict)
        answer = answer_dict['choices'][0]['text']
    except Exception as e:
        print(e)
        answer = "I'm sorry, but I'm currently unable to process your request. Please try again later."
    return answer
