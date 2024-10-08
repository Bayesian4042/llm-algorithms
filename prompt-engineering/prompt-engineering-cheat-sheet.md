# Introduction
In-Context learning or famously known as prompt engineering requires zero updates in model paramaters. It is just an input to the model, prompt guides the model to activate the parameters in the part of the model that contains the correct information. In essence, prompting is instruction given to the model to perform any downstream task. It is straightforward way to solve any problem as it doesn’t require expensive retraining of the model. Prompt engineering then would be the process of designing, templating, and refining a prompt to generate desired output from the model.

# Few Shot Prompting
The most common form of prompt engineering is few shot prompting. This is because it’s both simple to do and extremely effective. Few shot prompting is giving a couple examples of how you want the AI to act. Instead of searching for the tokens with the right distribution to get the response we want, we give the model several example distributions and ask it to mimic those. For example, if we wanted the model to do sentiment analysis defining reviews as positive or negative we could simply give it a few examples before the input.

consider the prompt below.
    ```
        consider the prompt below.

        Worked as advertised, 10/10: positive
        It was broken on delivery: negative
        Worth every penny spent: positive
        Overly expensive for the quality: negative
        If this is the best quality they can do, call me mr president: negative
        <Input data>:
    ```
In this example, we aren’t telling the model how to respond, but from the context the LLM can figure out that it needs to respond with either the word positive or negative. Of course, there could be an array of acceptable responses, in which case giving instructions beforehand can help improve the results. To do this, we might append to our few shot prompt above with the following phrase, “Determine the sentiment of each review as one of the following: (positive, negative, neutral, strongly positive, strongly negative)”. It’s also needed with most models, OpenAI included to include language to restrict the output, such as “Please respond with only one option from the list with no explanation.” You might wonder why we’d suggest you say words like “please” to a model. The answer is pretty simple: in the training data, the highest-quality and most-usefully-structured human-to-human conversations follow certain conventions of politeness that you’re likely familiar with, like saying please and thank you. The same results can be achieved by using an excess of profanity and deep jargon on a topic because flouting those politeness conventions is another huge part of the training set, although that strategy isn’t as consistent given that the companies training the models often “clean” their data of examples like that, regardless of their quality downstream.

This type of prompting can be very useful when you need your response to be formatted in a certain way. If we need our response in JSON or XML we could ask the model to return it in the format, but it likely will get the keys or typing wrong. We can easily fix that by instead just showing the model several samples of expected results. Of course, prompting the model to return JSON will work, but JSON is a very opinionated data structure and the model might hallucinate problems that are hard to catch, like using single quotes instead of double quotes. We’ll be going over tooling that can help with that later in the chapter.

The one major downside to few shot prompting is that examples can end up being quite long. For example, coding examples we might add and share can easily be thousands of tokens long, and that’s possible to define a single function. Giving an example of an entire class, file, or project can easily push us out of our limits. Many models still have context limits restricted to 2k, 4k, or 8k. Since token limits are often restrictive, it can be difficult to balance adding another example or giving the user more space. Also, we often pay per token so few shot prompting can be much more expensive than other prompting techniques. Because of this, many have turned to one shot prompting, to be more efficient and save money.

# One Shot Prompting
One-shot learning is a machine learning concept where a model is expected to make accurate predictions given only a single example of each new class during training. In the context of Large Language Models and prompting, one-shot refers to situations where the model has to understand and execute a task based on a single, clear instruction or example in the prompt, often without having seen similar examples during training. It's the effort of crafting the perfect example to get the expected results.

Consider our sentiment analysis example above, if you gave a model only one positive example, you’re likely to bias the model to only give positive classifications. Especially if the model never saw such a problem before. So how can one shot prompting ever be achieved? Thankfully, while this seems impossible at the outset, it’s actually quite achievable. Afterall, few shot prompting is very effective, but follows the law of diminishing returns. Each new example improves only marginally. The first example always does the most lifting.

LLMs can perform well on one-shot tasks due to the extensive pre-training they undergo on large and diverse datasets. During this pre-training, the models learn a wide array of language patterns, concepts, and structures, giving them a broad understanding of language and the world. When given a new one-shot task, they leverage this learned understanding to comprehend the task and generate a response, even if the exact task was not part of their training data. Here’s an example of a prompt attempting to coerce the model using one shot prompting to respond to a word problem correctly:

    ```
        User: Answer this question. Think it through step by step, so that we know it’s correct:
        A dad and his son were in an accident and rushed to a hospital. The man’s son was in the operating room and the doctor said, “I can’t operate on you. You’re my son.” How is that possible?
        Assistant: The son and the father were both injured, meaning that the only other person that the doctor could be and still have the same son is the father’s spouse, maybe a mother, or another father perhaps.
        User: Answer this question. Think it through step by step, so that we know it’s correct:
        How could it be possible to be your own grandpa?
        Assistant:
    ```
the ability of LLMs to handle one-shot tasks improves as they are scaled up—as the model size increases and they are trained on more diverse and larger datasets, their capacity to generalize from their training to unseen one-shot tasks also improves. Nonetheless, it's worth noting that while LLMs can perform impressively on one-shot tasks, they are not perfect and their performance can still vary based on the complexity and specificity of the task. Despite this, one shot prompting generally needs much less data and only one example to craft. This can make them more accessible, faster to craft, and easier to experiment with. Because of this it has led researchers to push the boundaries even further.

# Zero Shot Prompting
Zero shot prompting is figuring out how to craft a prompt to get use the expected results without giving any examples. Zero shot prompts often don't perform as consistently as few-shot or one-shot prompts.

Most zero shot prompts take advantage of "Chain-of-Thought". The chain-of-thought paper showed that by encouraging models to follow step by step process, reasoning through multiple steps instead of jumping to the conclusion, LLM were more likely to correctly answer the math problems. By appending four magic words to the end of our prompts, "think step by step", models transformed from dunces into puzzle solving olympiads. Of course, it came with some issues. As thinking through multiple steps led to longer responses and a less ideal user experience.

There isn't of course a perfect zero shot prompt yet and it's a continuing part of research. One interesting paper proposed an interesting strategy they termed Thread of Thought. Essentially they figured they could do better than just "think step by step"if they just a few words. So they generated 30 variations of the phrase and ran evaluations to determine which one worked best. From their work they proposed "walk me through this context in manageabke parts step by step, summarizing and analysizing as we go". Would give better result when working with GPT-4. It's hard to know if this prompt works equally well with other models.

Some other notable findings have left researches shocked that the approach worked, or example, offering an imaginary tip to a model will return better results. In addition, the authors have found strategies like telling the model you’ll lose your job if it doesn’t help you or even threatening to fire the model if it does a terrible job has elicited better results. Similar to the original “think step by step”, asking the model to “take a deep breath” can also ensure better outputs particularly in math problems. It seems most strategies humans use, or use on other humans, to produce better work are fair game. Of course, the best trick will depend on which model you use and the underlying data it was trained on.

# Prompt Engineering Basics

There are several challenges with prompt engineering over regular prompting. For example, prompt engineering relies particularly upon knowing the format the user expects the answer to be in. With prompting you are the user, so you can just keep trying till you see an answer you like, that doesn’t fly in prompt engineering.

A bigger issue is that when building an application, your end users will have varying levels of knowledge on how to craft a prompt. Some may not have any skill and will struggle to get good responses, and others will have so much skill they will likely try to persuade your LLM to go off the rails you’ve set for it. Regardless, our goal is to build railings in such a way that skilled users won’t be able to derail your application and unskilled users will have a smooth ride. A user’s skill in crafting a prompt shouldn’t be the determining factor of a successful experience.

a good prompt engineer should be able to tell you rather quickly whether or not the solution you are trying to build can be done with prompt engineering at all. Even utilizing advanced techniques like RAG there are limitations on what you can do with prompt engineering alone. Knowing when you need to send a model back for additional finetuning is invaluable and can save your team from spinning their wheels for weeks without any progress.

# Anatomy of Prompt
To an engineer, a prompt is made up of a few elements, and identifying these elements makes it easier to create a framework to solve your use case and provide a better example for your users. Let’s say we are building an internal chatbot for our company to help answer HR related questions based on internal documentation. One prompt we might expect from a user would be, “How much does the company match for our 401k?”. This is the first element to a prompt, the input or user’s prompt. If you have only ever used LLM apps and have never built them, this is likely all you’ve ever seen. Generally the input is gathered from a free form text box and so it’s important to note that it can almost be anything. Oftentimes it will be awful, riddled with typos and mistakes, and not written in a manner to speak to a bot but to speak to another human.
    Real example in which the bot responded in the most probable way to user's satisfaction.
    LLM response : ```
        System: You are a helpful assistant who knows about all company policies at XYZ company. Be courteous and keep conversations strictly related to the company. Offer links when available so users can look at the documentation themselves.
    User: How much does the company match for our 401k?
    Context: <Examples from a VectorDB search for closest document> System: Strictly answer the user’s question, and only if it relates to company policies. If you don’t know the answer, simply say so. Be courteous and keep conversations strictly related to the company. Assistant: Sure, I can help you with that! The company currently offers a 4% match to your 401k. You can find more details...

    ```
Giving an LLM information in a structured format improves the model’s chance of responding correctly. So let’s break down what we are seeing.

First, to improve results, we will often take the user’s prompt and inject it into an instruction set or template. One of the most basic templates and a great example is the Q&A bot template which we showed earlier and would have looked like this: “Q: How much does the company match for our 401k? A:”. Generally, in this section though there will be an instruction given to direct the model. This doesn’t have to be much, but oftentimes it will be much more detailed. For example, “Answer the following question and explain it as if the user was a five year old. Q: How much does the company match for our 401k? A:”.

The next element is the context the model will need to respond appropriately. In our example, it’s very likely we haven’t finetuned a model to actually know XYZ’s company policies. What we need to do is give it to the model inside the prompt. In our example, we are likely doing this with RAG and where we would add the results from a semantic search.

Context can be lots of different things though, and not just RAG search results. It could be the current time, weather information, current events, or even just the chat history. You will often also want to include some database look up information about the user to provide a more personalized experience. All of this is information we might look up at the time of query, but context can often be static. For example, one of the most important pieces of information to include in the context is examples to help guide the model via few shot or one shot prompting. If your examples are static and not dynamic though, they likely are just hard coded into the instruction template. The context often contains the answers to the users’ query and we are simply using the LLM to clean, summarize, and format an appropriate response. Ultimately, any pragmatics the model lacks will need to be given in the context.
The last element is the system prompt. The system prompt is a prompt that will be appended and used on every request by every user. It is designed to give a consistent user experience. Generally, it’s where we would include role prompting or style prompting. Some examples of such role prompting or style prompting could include:
    ```
        Take this paragraph and rephrase it to have a cheerful tone and be both informative and perky.
        You are a wise old owl who helps adventurers on their quest.
        In the form of a poem written by a pirate.
    ```
    ```
        PARTS OF THE PROMPT .
        Input - what the user wrote, can be anything.
        Instruction - the template used, often containing detail and instructions to guide the model.
        Context - pragmatics the model needs to respond appropriately (e.g. examples, database lookups, RAG).
        System prompt - specific instruction given to the model on every request to enforce a certain user experience (e.g. talk like a pirate).
    ```

# Prompting Hyperparameters
Another aspect of prompt engineering you won’t see with simple prompting is prompt hyperparameter tuning. There are several hyperparameters you can set when making a query in addition to the prompt to increase or decrease the diversity of responses. Depending on your objective, the value of these parameters can greatly improve or even be a detriment to the query results for your users.

## Temperature
The temperature parameter determines the level of randomness your model will account for when generating tokens. Setting it to zero will ensure the model will always respond the exact same way when presented with identical prompts. This is critical for jobs where we want our results to be predictable, but can leave our models stuck in a rut. Setting it to a higher value will make it more creative. Setting it negative will tell it to give you the opposite response to your prompt.

To understand this parameter better, it might help to look closer at how a model is determining the next token. In below figure, there is an example of this process. Given the input "Iam a", a language model will genrate a list of probabilities for each token. These probabilities show the likelihood that each token will be chosen.

Temperature is applied during the softmax algorithm, a higher temperature will flatten out the probability distribution giving less weight to tokens with large logits, and more weights to tokens with smaller logits. A lower temperature does the opposite. A temperature of zero is actually impossible, since we can’t divide by zero. Instead we run an argmax algorithm ensuring we simply just pick the token with the highest logit.

## Number of beams
## Top K
## Top P

# Prompt Enginerring Tooling
## LangChain
## Guidance
Guidance is an open source library that comes from Microsoft that enforces programmatic responses.   Guidance seeks to constrain the response space, setting custom stopping tokens, and complex templating.

## DSPy

# Advanced Prompt Engineering Techniques
## Giving LLMs Tools
What if instead of a complicated prompt engineering system, we instead just give our model access to the internet? If it knows how to search the internet then it can always find up-to-date information. While we are at it, we can give it access to a calculator so we don’t have to waste CPU cycles having the LLM itself do basic math. We can give it access to a clock so it knows the current time and maybe even a weather app so it can tell the weather. The sky's the limit! We just need to train the model how to use tools, and that’s where Toolformers comes in.

we can use clever prompt engineering to introduce new tools using LangChain or Guidance.
## ReAct
Reasoning and Acting (ReAct) is a few-shot framework for prompting that is meant to emulate the way that people reason and make decisions when learning new tasks.[14] It involves a multi-step process for the LLM, where a question is asked, the model determines an action, then observes and reasons upon the results of that action in order to determine subsequent actions.
An example could look like this:
    ```
        Question: What is the airspeed velocity of an unladen African swallow compared to a European swallow with the same load?
        Thought 1: I need to search for airspeed velocity of a European swallow, so I can compare it with an African swallow.
        Action 1: Search[European Swallow airspeed velocity]
        Observation 1: We need to know the Strouhal number in order to determine airspeed. The bird's Strouhal number converges between 0.2 and 0.4.
    ```

As you can see in this example, the purpose of ReAct is to force the model to think before it acts. This isn’t much different from the other prompting methods we have discussed. The big difference is that we allow the model to take actions. In our example above, this included a “Search” action, or essentially an ability to look up information on the internet as a human would

# Summary
- The most straightforward approach to prompting is to just give a model examples of what you want it to do.
- The more examples you can add to a prompt the more accurate your results will be.
- The fewer examples you need to add, the more general and all purpose your prompt will be.
- The four parts of a prompt are:
    - Input - this is what the user writes.
    - Instruction - this is the template with task specific information encoded. 
    - Context - this is information you add through RAG or other database lookups.
    - System - specific instructions given for every task, should be hidden from the user.
- Knowing your training data will help you craft better prompts by choosing a word order that matches the training data.
- LangChain is a popular tool that allows us to create chains or pipelines to utilize LLMs in an engineering fashion.
- Guidance is a powerful tool that gives us more fine grained control over the LLMs actual generated text.
- Toolformers taught LLMs how to use tools which gives them access to accomplish previously impossible tasks.
- ReAct is a few-shot framework for prompting that is meant to emulate the way that people reason and make decisions when learning new tasks.
