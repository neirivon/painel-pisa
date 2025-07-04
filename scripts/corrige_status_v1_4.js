db.rubrica_sinapse.updateOne(
  { versao: "v1.4", status: "ativa" },
  { $set: { status: "inativa" } }
);

db.rubrica_sinapse.updateMany(
  { versao: "v1.5" },
  { $set: { status: "inativa" } }
);

db.rubrica_sinapse.updateOne(
  { _id: ObjectId("6855302b05ffe0ff8c0f508b") },
  { $set: { status: "ativa" } }
);

