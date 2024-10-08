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


