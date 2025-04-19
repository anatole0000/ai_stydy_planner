from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import numpy as np
from .models import StudySession

def recommend_topic(user):
    # Fetch study session data for the user
    study_sessions = StudySession.objects.filter(user=user)

    # Prepare the study data with encoded topic and study time
    study_data = []
    topics = []
    for session in study_sessions:
        study_data.append([session.study_time, session.user.id])  # Only keep study time and user ID
        topics.append(session.topic)  # Save the topic for encoding later

    # Encode the topics using LabelEncoder
    encoder = LabelEncoder()
    encoded_topics = encoder.fit_transform(topics)

    # Combine encoded topics with study times and user IDs
    study_data = np.array([study_data[i] + [encoded_topics[i]] for i in range(len(study_data))])

    # Now, study_data has 3 features: [study_time, user_id, encoded_topic]
    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=3, random_state=0)
    kmeans.fit(study_data)  # Study time + encoded topic + user ID for clustering

    # Example: Find the cluster the user belongs to (based on study time and topic)
    user_data = np.array([30, 0, 0])  # Example: User studying "Math" (encoded as 0) for 30 minutes
    user_cluster = kmeans.predict([user_data])

    # Get recommended topics from the user's cluster (or apply custom logic)
    recommended_topics = encoder.inverse_transform(user_cluster)  # Decode back to the topic names
    return recommended_topics[0]
