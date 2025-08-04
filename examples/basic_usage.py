"""Basic usage examples for WIBA Python client."""

import os
from wiba import WIBA

def main():
    """Demonstrate basic WIBA client usage."""
    
    # Initialize client (API token from environment or parameter)
    api_token = os.getenv('WIBA_API_TOKEN', 'your_token_here')
    client = WIBA(api_token=api_token)
    
    # Example texts
    texts = [
        "Climate change requires immediate action from governments worldwide.",
        "The weather is nice today.",
        "We must invest in renewable energy to reduce carbon emissions.",
        "I had lunch at noon.",
        "Nuclear power plants pose significant safety risks to communities."
    ]
    
    print("🔍 WIBA Client Demo")
    print("=" * 50)
    
    # 1. Argument Detection
    print("\n1. Argument Detection:")
    print("-" * 30)
    
    detection_results = client.detect(texts)
    for result in detection_results:
        status = "✓ Argument" if result.is_argument else "✗ Not an argument"
        print(f"{status} (conf: {result.confidence:.3f}): {result.text[:60]}...")
    
    # 2. Topic Extraction (only for arguments)
    print("\n2. Topic Extraction:")
    print("-" * 30)
    
    argument_texts = [result.text for result in detection_results if result.is_argument]
    if argument_texts:
        extraction_results = client.extract(argument_texts)
        for result in extraction_results:
            print(f"Topic: '{result.topic}' | Text: {result.text[:60]}...")
    else:
        print("No arguments found for topic extraction.")
    
    # 3. Stance Analysis
    print("\n3. Stance Analysis:")
    print("-" * 30)
    
    stance_examples = [
        ("Solar panels are becoming more affordable", "renewable energy"),
        ("Coal power plants are reliable", "renewable energy"),
        ("Nuclear waste is dangerous", "nuclear power")
    ]
    
    for text, topic in stance_examples:
        stance_result = client.stance(text, topic)
        if stance_result:
            result = stance_result[0]  # Single result
            print(f"Stance: {result.stance} | Topic: {result.topic} | Text: {result.text[:40]}...")
    
    # 4. Argument Discovery
    print("\n4. Argument Discovery:")
    print("-" * 30)
    
    long_text = """
    Climate change is one of the most pressing issues of our time. The scientific evidence is overwhelming. 
    Rising global temperatures are causing sea levels to rise and weather patterns to become more extreme. 
    We must transition to renewable energy sources immediately. However, some argue that the economic costs 
    are too high. This is a short-sighted view that ignores the long-term benefits. The weather forecast 
    shows rain tomorrow. Clean energy technologies are creating jobs and driving innovation. Critics claim 
    that renewable energy is unreliable, but advances in battery storage are solving this problem.
    """
    
    discovery_results = client.discover_arguments(long_text.strip())
    if discovery_results and len(discovery_results) > 0:
        print(f"Found {len(discovery_results)} argumentative segments:")
        for i, segment in enumerate(discovery_results[:3], 1):  # Show first 3
            print(f"  {i}. (conf: {segment.confidence:.3f}) {segment.text[:80]}...")
    else:
        print("No argumentative segments found.")
    
    # 5. Client Statistics
    print("\n5. Client Statistics:")
    print("-" * 30)
    stats = client.get_statistics()
    print(f"Total requests: {stats.total_requests}")
    print(f"Texts processed: {stats.total_texts_processed}")
    print(f"Method calls: {stats.method_calls}")

if __name__ == "__main__":
    main()