import torch
from transformers import AutoModel, AutoTokenizer
from PIL import Image
import logging
import io

logger = logging.getLogger(__name__)

class DeepSeekOCR:
    def __init__(self, model_name: str = "deepseek-ai/deepseek-vl-1.3b-chat", device: str = None):
        """
        Initialize DeepSeek OCR model.
        
        Args:
            model_name: HuggingFace model name (default: deepseek-vl-1.3b-chat for efficiency)
            device: 'cuda' or 'cpu'. If None, auto-detects.
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Initializing DeepSeek OCR on {self.device}...")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            self.model = AutoModel.from_pretrained(
                model_name, 
                trust_remote_code=True,
                torch_dtype=torch.bfloat16 if self.device == "cuda" else torch.float32
            ).to(self.device)
            self.model.eval()
            logger.info("DeepSeek OCR model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load DeepSeek model: {e}")
            raise

    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extract text from an image using DeepSeek VL.
        """
        try:
            # Load image
            pil_image = Image.open(image_path).convert("RGB")
            
            # Prepare conversation
            conversation = [
                {
                    "role": "User",
                    "content": "<image_placeholder>Extract all text from this image and format it as markdown.",
                    "images": [pil_image]
                },
                {
                    "role": "Assistant",
                    "content": ""
                }
            ]
            
            # Process inputs
            prepare_inputs = self.tokenizer.apply_chat_template(
                conversation, 
                add_generation_prompt=True, 
                return_tensors="pt"
            ).to(self.model.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    prepare_inputs,
                    max_new_tokens=1024,
                    do_sample=False,
                    use_cache=True
                )
                
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract the assistant's response (remove the prompt)
            # This logic depends on the exact output format of the model
            # Usually we can split by "Assistant:" or similar if needed, 
            # but apply_chat_template usually handles the prompt structure.
            # We might need to post-process to get just the new text.
            
            # Simple heuristic: return the whole thing or try to strip prompt if possible
            # For now, returning the whole decoded string is safer for debugging
            return response

        except Exception as e:
            logger.error(f"OCR failed for {image_path}: {e}")
            return ""
