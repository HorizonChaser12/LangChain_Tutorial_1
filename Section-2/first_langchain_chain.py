import langchain_openai
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

load_dotenv()


def main():
    model = langchain_openai.ChatOpenAI(model="gpt-5", temperature=0.7)
    # model = ChatOllama(model="gemma3", temperature=0.7)
    
    information = """ Elon Reeve Musk FRS (/ˈiːlɒn/ EE-lon; born June 28, 1971) is an international businessman and entrepreneur known for his leadership of Tesla, SpaceX, X (formerly Twitter), and the Department of Government Efficiency (DOGE). Musk has been the wealthiest person in the world since 2021; as of May 2025, Forbes estimates his net worth to be US$424.7 billion.

    Born to a wealthy family in Pretoria, South Africa, Musk emigrated in 1989 to Canada; he had obtained Canadian citizenship at birth through his Canadian-born mother. He received bachelor's degrees in 1997 from the University of Pennsylvania in Philadelphia, United States, before moving to California to pursue business ventures. In 1995, Musk co-founded the software company Zip2. Following its sale in 1999, he co-founded X.com, an online payment company that later merged to form PayPal, which was acquired by eBay in 2002. That year, Musk also became an American citizen.

    Musk's political activities, views, and statements have made him a polarizing figure, especially following the COVID-19 pandemic. He has been criticized for making unscientific and misleading statements, including COVID-19 misinformation and promoting conspiracy theories, and affirming antisemitic, racist, and transphobic comments. His acquisition of Twitter was controversial due to a subsequent increase in hate speech and the spread of misinformation on the service. His role in the second Trump administration attracted public backlash, particularly in response to DOGE."""


    summary_prompt = """ Given the information {information} about a person who is there in real life I want you to create:
    1. a short summary
    2. two most interesting facts about them
    """

    summary_prompt_template = PromptTemplate(template=summary_prompt, input_variables=['information'],validate_template=True)
    
    chain = summary_prompt_template | model
    response  = chain.invoke(input={"information":information})
    print(response.content)


if __name__ == "__main__":
    main()
