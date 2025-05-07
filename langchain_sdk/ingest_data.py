from langsmith import Client

def ingest_data(dataset_name, inputs):
    """
    Ingest data into Langsmith by creating a dataset and adding examples.
    """
    client = Client()

    # Create dataset
    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="Langsmith evaluation dataset for Game of Thrones questions and answers.",
    )

    # Add examples to the dataset
    for question, answer in inputs:
        client.create_example(
            inputs={"question": question},
            outputs={"answer": answer},
            dataset_id=dataset.id,
        )

    print(f"Dataset '{dataset_name}' created successfully.")

if __name__ == "__main__":
    dataset_name = "LS_EVAL"
    
    questions = [
        "What is the significance of Jon Snow's parentage in the storyline?",
        "How does Daenerys Targaryen's journey shape her character development?",
        "What role does Tyrion Lannister play in the political dynamics of Westeros?",
    ]

    correct_answers = [
        "Jon Snow's parentage reveals he is the son of Lyanna Stark and Rhaegar Targaryen, giving him a legitimate claim to the Iron Throne and a key role in uniting factions against the White Walkers.",
        "Daenerys Targaryen's journey transforms her from an exiled princess to a powerful leader, as she faces betrayal, loss, and the moral challenges of ruling the Seven Kingdoms.",
        "Tyrion Lannister uses his wit and intelligence to navigate the dangerous politics of Westeros, often acting as a voice of reason while dealing with prejudice and family conflicts."
    ]

    inputs = [
        (questions[0], correct_answers[0]),
        (questions[1], correct_answers[1]),
        (questions[2], correct_answers[2]),
    ]
    print("Starting to ingest data...")
    try:
        ingest_data(dataset_name, inputs)
    except Exception as e:
        print(f"An error occurred while ingesting data: {e}")
    

