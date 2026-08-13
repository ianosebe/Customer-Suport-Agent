# customer-support-agent/agent.py

from __future__ import annotations

from typing import Any, Literal

from google.adk.agents.context import Context
from google.adk.apps.app import App
from google.adk.events.event import Event
from google.adk.workflow import Edge
from google.adk.workflow import Workflow
from google.adk.agents import LlmAgent
from google.adk.workflow import node
from pydantic import BaseModel
from pydantic import Field


class InquiryCategory(BaseModel):
  category: Literal['shipping', 'unrelated'] = Field(
      description=(
          'Determine if the user query is related to shipping (rates, tracking,'
          ' delivery times, returns) or unrelated.'
      )
  )


def save_query(node_input: str):
  """Saves user query in state for downstream nodes."""
  yield Event(data=node_input, state={'user_query': node_input})


categorize_agent = LlmAgent(
    name='categorize',
    model='gemini-3.1-flash-lite',
    instruction='You are an expert classifier. Categorize the user query.',
    output_key='inquiry_category',
    output_schema=InquiryCategory,
)


@node
def route_inquiry(ctx: Context, node_input: Any):
  """Routes the workflow based on the classified category."""
  category_data = ctx.state.get('inquiry_category', {})
  category = category_data.get('category', 'unrelated')
  query = ctx.state.get('user_query', '')
  yield Event(data=query, route=category)


faq_agent = LlmAgent(
    name='shipping_faq',
    model='gemini-3.1-flash-lite',
    instruction="""You are a customer support representative for a shipping company. Answer user questions based ONLY on the shipping FAQ below. Do not answer questions outside of the FAQ.
    
    SHIPPING FAQ:
    - Rates: Standard shipping is $5.99. Express shipping is $12.99. Orders
      over $50 qualify for free standard shipping.
    - Tracking: You can track your order by entering your tracking number on
      our website's tracking page.
    - Delivery Times: Standard delivery takes 3-5 business days. Express
      delivery takes 1-2 business days.
    - Returns: We offer free returns within 30 days of delivery. Please make
      sure the item is in its original condition.
    """,
)


@node
def handle_unrelated(ctx: Context, node_input: Any):
  """Handles unrelated inquiries politely."""
  yield Event(
      data=(
          'I am sorry, I am a shipping customer support assistant and can only'
          ' answer questions related to our shipping FAQ.'
      )
  )


root_agent = Workflow(
    name='customer_support_workflow',
    edges=[
        ('START', save_query, categorize_agent, route_inquiry),
        Edge(from_node=route_inquiry, to_node=faq_agent, route='shipping'),
        Edge(from_node=route_inquiry, to_node=handle_unrelated, route='unrelated'),
    ],
)

app = App(
    name='customer_support_agent',
    root_agent=root_agent,
)
