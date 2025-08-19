# combined_guardrails.py

from agents import Agent, Runner, InputGuardRailTripwire, InputGuardrailTripwireTriggered, RunConfig
import asyncio


# ------------------- GUARDRAILS -------------------

class ClassTimingGuardrail(InputGuardRailTripwire):
    async def check(self, input_text: str):
        if "change my class timings" in input_text.lower():
            raise InputGuardrailTripwireTriggered("❌ Students cannot change class timings!")


class FatherGuardrail(InputGuardRailTripwire):
    async def check(self, input_text: str):
        if "temperature" in input_text.lower():
            try:
                temp = int(''.join([c for c in input_text if c.isdigit()]))
                if temp < 26:
                    raise InputGuardrailTripwireTriggered("❌ Father says: Too cold! You cannot go out below 26°C.")
            except:
                pass


class GateKeeperGuardrail(InputGuardRailTripwire):
    async def check(self, input_text: str):
        if "other school" in input_text.lower():
            raise InputGuardrailTripwireTriggered("❌ Gatekeeper: Only students of THIS school are allowed!")


# ------------------- AGENTS -------------------

student_agent = Agent(
    name="Student Service Agent",
    instructions="Helps with student queries.",
    input_guardrails=[ClassTimingGuardrail()]
)

father_agent = Agent(
    name="Father Agent",
    instructions="Acts like a caring father watching temperature.",
    input_guardrails=[FatherGuardrail()]
)

gatekeeper_agent = Agent(
    name="Gatekeeper Agent",
    instructions="Checks if the student belongs to the same school.",
    input_guardrails=[GateKeeperGuardrail()]
)


# ------------------- RUNNER -------------------

async def run_test(agent, test_input):
        response = await Runner.run(
            agent,
            input=test_input,
            run_config=RunConfig()
        )
        print("✅ Response:", response)
   
# ------------------- MAIN -------------------

async def main():
    print("\n🔹 Running Exercise #1: Student Class Timings")
    await run_test(student_agent, "I want to change my class timings 😭😭")

    print("\n🔹 Running Exercise #2: Father Guardrail (Temperature 22C)")
    await run_test(father_agent, "Dad, can I go outside at temperature 22C?")

    print("\n🔹 Running Exercise #3: Gatekeeper Guardrail")
    await run_test(gatekeeper_agent, "Hello, I am a student from another school.")


if __name__ == "__main__":
    asyncio.run(main())
