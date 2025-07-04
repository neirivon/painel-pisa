// Conecta à coleção
const collection = db.getCollection("rubrica_sinapse");

// Lista de ObjectIds das duplicatas inativas a serem removidas (exceto a ativa)
const duplicatasInativas = collection.find({
  versao: "v1.5",
  status: "inativa"
}).toArray();

// Se houver duplicatas inativas
if (duplicatasInativas.length > 0) {
  const idsParaRemover = duplicatasInativas.map(doc => doc._id);
  const resultado = collection.deleteMany({ _id: { $in: idsParaRemover } });

  print(`🗑️ Removidos ${resultado.deletedCount} documentos duplicados inativos da versão v1.5.`);
} else {
  print("✅ Nenhuma versão duplicada inativa da v1.5 encontrada.");
}

