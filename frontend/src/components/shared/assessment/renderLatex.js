import katex from 'katex'
import 'katex/dist/katex.min.css'

// Renders inline LaTeX delimited by $...$ or $$...$$; falls back to escaped text.
export function renderLatex(text){
  if(!text) return ''
  // Simple replace: find $...$ segments and render individually.
  return text.replace(/\$(.+?)\$/g, (_, expr)=>{
    try { return katex.renderToString(expr, { throwOnError:false }) } catch { return expr }
  })
}
