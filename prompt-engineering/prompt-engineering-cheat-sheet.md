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


