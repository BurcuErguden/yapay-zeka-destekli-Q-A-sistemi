from pinecone import Pinecone, ServerlessSpec

# Pinecone'a bağlanıyoruz
pc = Pinecone(api_key='4aecf571-c379-4fa5-962d-fcdd03bd4bc6', environment='us-west-2')

indeks_adi = 'benimindeks'
pc.create_index(
    name=indeks_adi,
    dimension=3,  #vektör boyutlarımız 3
    metric='euclidean',
    spec=ServerlessSpec(
        cloud='aws',
        region='us-east-1'
    )
)

print(f"{indeks_adi} indeksi oluşturuldu.")

indeks = pc.Index(indeks_adi)

# Analiz sonucunda vektör haline getirdiğimiz verilerimizi yükleyelim
veri = [{'id': '192.168.1.1', 'values': [25.0, 1136.6, 11.0]}, 
        {'id': '192.168.1.2', 'values': [35.0, 1267.8857142857144, 10.0]}, 
        {'id': '192.168.1.3', 'values': [39.0, 886.3589743589744, 13.0]}
]
vectors = [(item['id'], item['values']) for item in veri]
indeks.upsert(vectors=vectors)
print("Veriler Pinecone'a yüklendi.")

