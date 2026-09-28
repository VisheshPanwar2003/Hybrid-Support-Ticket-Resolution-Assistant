from llm.chain import ask_assistant

def main():
    print("===========================================")
    print(" 🚀 HYBRID TICKET RESOLUTION ASSISTANT 🚀 ")
    print("===========================================")
    print("Type 'exit' or 'quit' to stop the assistant.\n")
    
    while True:
        # Get custom input from the user
        user_query = input("▶️  USER QUERY: ").strip()
        
        # Check for exit commands
        if user_query.lower() in ['exit', 'quit']:
            print("Shutting down assistant. Goodbye!")
            break
            
        if not user_query:
            continue
            
        print("-" * 40)
        
        # Pass the custom query to your hybrid pipeline
        answer = ask_assistant(user_query)
        
        # Print the final result cleanly
        if not answer.startswith("System:"):
            print("\n🤖 FINAL ANSWER:")
            print(answer)
        else:
            print(f"\n🤖 {answer}")
        
        print("\n" + "=" * 43 + "\n")
            
if __name__ == "__main__":
    main()