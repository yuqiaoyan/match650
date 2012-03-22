import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryParser.ParseException;
import org.apache.lucene.queryParser.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.RAMDirectory;
import org.apache.lucene.util.Version;

import java.io.IOException;

public class HelloLucene {
  public static void main(String[] args) throws IOException, ParseException {
    // 0. Specify the analyzer for tokenizing text.
    //    The same analyzer should be used for indexing and searching
    StandardAnalyzer analyzer = new StandardAnalyzer(Version.LUCENE_35);

    // 1. create the index
    Directory index = new RAMDirectory();

    IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_35, analyzer);

    IndexWriter w = new IndexWriter(index, config);
    addDoc(w, "social network analysis");
    addDoc(w, "social interests");
    addDoc(w, "Managing Gigabytes");
    addDoc(w, "The Art of Computer Science");
    w.close();

    // 2. query
    String querystr = args.length > 0 ? args[0] : "social";

    // the "title" arg specifies the default field to use
    // when no field is explicitly specified in the query.
    Query q = new QueryParser(Version.LUCENE_35, "interests", analyzer).parse(querystr);

    // 3. search
    int hitsPerPage = 10;
    IndexSearcher searcher = new IndexSearcher(index, true);
    TopScoreDocCollector collector = TopScoreDocCollector.create(hitsPerPage, true);
    searcher.search(q, collector);
    ScoreDoc[] hits = collector.topDocs().scoreDocs;
    
    // 4. display results
    System.out.println("Found " + hits.length + " hits.");
    for(int i=0;i<hits.length;++i) {
      int docId = hits[i].doc;
      Document d = searcher.doc(docId);
      System.out.println((i + 1) + ". " + d.get("title"));
    }

    // searcher can only be closed when there
    // is no need to access the documents any more. 
    searcher.close();
  }

  public enum fieldName{
      INTERESTS,
      AFFILIATION
  }
  
  String fieldNameStrings[] = {"INTERESTS", "AFFILIATION"};
  
  private static void addField(Document profile, String userField, String value){
  //adds the field to the index
      if(userField.equals("interests"))
         profile.add(new Field("interests",value,Field.Store.YES,Field.Index.NO));
         else if (userField.equals("affiliation"))
              profile.add(new Field("affiliation",value,Field.Store.YES,Field.Index.NOT_ANALYZED));
         else
             profile.add(new Field("content",value,Field.Store.YES,Field.Index.ANALYZED));
  }
  
  private static void addDoc(IndexWriter w, String value) throws IOException {
    Document doc = new Document();
        String test = "interests";
        String affiliationTest = "affiliations";
        String contentTest = "content";
        addField(doc,test,value);
        addField(doc,affiliationTest,"university of michigan");
        addField(doc,contentTest, "university of michigan"+value);
        //doc.add(new Field("title", value, Field.Store.YES, Field.Index.ANALYZED));
    w.addDocument(doc);
  }
}
