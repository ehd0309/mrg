export const queryKeys = {
  documents: {
    list: () => ["documents"],
    byId: (id: string) => ["documents", id],
    inputFile: (id: string) => ["input-file", "documents", id],
    outputFile: (id: string) => ["output-file", "documents", id],
  },
};
