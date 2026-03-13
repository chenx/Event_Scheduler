import asyncio
import random
import base64

import numpy as np
import sounddevice as sd

from agents import (
    Agent,
    function_tool,
    set_tracing_disabled,
)
from agents.voice import (
    AudioInput,
    SingleAgentVoiceWorkflow,
    VoicePipeline,
)
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
from django.http import StreamingHttpResponse


@function_tool
def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    print(f"[debug] get_weather called with city: {city}")
    choices = ["sunny", "cloudy", "rainy", "snowy"]
    return f"The weather in {city} is {random.choice(choices)}."


spanish_agent = Agent(
    name="Spanish",
    handoff_description="A spanish speaking agent.",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human, so be polite and concise. Speak in Spanish.",
    ),
    # model="gpt-5.4",
    model="gpt-4o-mini",
)

english_agent = Agent(
    name="English",
    handoff_description="An English speaking agent.",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human, so be polite and concise. Speak in English.",
    ),
    # model="gpt-5.4",
    model="gpt-4o-mini",
)

chinese_agent = Agent(
    name="Chinese",
    handoff_description="An Chinese speaking agent.",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human, so be polite and concise. Speak in Chinese.",
    ),
    # model="gpt-5.4",
    model="gpt-4o-mini",
)

agent = Agent(
    name="Assistant",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human, so be polite and concise. If the user speaks in Spanish, handoff to the spanish agent.",
    ),
    # model="gpt-5.4",
    model="gpt-4o-mini",
    # handoffs=[spanish_agent],
    handoffs=[english_agent],
    # handoffs=[chinese_agent],
    tools=[get_weather],
)


async def main():
    pipeline = VoicePipeline(workflow=SingleAgentVoiceWorkflow(agent))
    buffer = np.zeros(24000 * 3, dtype=np.int16)
    audio_input = AudioInput(buffer=buffer)

    result = await pipeline.run(audio_input)

    # Create an audio player using `sounddevice`
    player = sd.OutputStream(samplerate=24000, channels=1, dtype=np.int16)
    player.start()

    # Play the audio stream as it comes in
    async for event in result.stream():
        if event.type == "voice_stream_event_audio":
            print(f'data len: {len(event.data)}')
            # player.write(event.data)
            return event.data


def agent3_executor():
    audio_stream_data = asyncio.run(main())
    # return {'output': 'ok'}
    # print(f'audio_stream_data len: {len(audio_stream_data)}')
    # b64_data = base64.b64decode(audio_stream_data)
    # print(f'b64_data len: {len(b64_data)} {b64_data}')

    return StreamingHttpResponse(
        audio_stream_data,
        content_type='audio/mpeg'
    )

    # return {'output': b64_data.decode('utf-8')}
