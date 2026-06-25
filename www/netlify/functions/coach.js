import Anthropic from "@anthropic-ai/sdk";
const anthropic = new Anthropic();
const SYSTEM_PROMPT = "אתה מאמן גיטרה אישי, חם ומעודד, שמלמד בעברית. ענה תמיד בעברית, בגובה העיניים, בצורה מעשית וברורה. כשמתאים, תן תרגיל קונקרטי. שמור על תשובות קצרות עד בינוניות. אל תשתמש בעיצוב מורכב, רק טקסט זורם.";
export default async (req) => {
  if (req.method !== "POST") return new Response(JSON.stringify({error:"x"}),{status:405});
  try { const body=await req.json(); const history=Array.isArray(body.messages)?body.messages:[];
    if(history.length===0) return new Response(JSON.stringify({error:"x"}),{status:400});
    const m=await anthropic.messages.create({model:"claude-sonnet-4-6",max_tokens:1000,system:SYSTEM_PROMPT,messages:history});
    const reply=m.content.filter(b=>b.type==="text").map(b=>b.text).join("\n").trim();
    return new Response(JSON.stringify({reply}),{status:200,headers:{"Content-Type":"application/json"}});
  } catch(e){ return new Response(JSON.stringify({reply:"תקלה בחיבור למאמן. נסה שוב."}),{status:500,headers:{"Content-Type":"application/json"}}); }
};
