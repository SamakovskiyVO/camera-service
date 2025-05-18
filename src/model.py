import torch

class QualityModel:
    def __init__(self, path: str, device: str = "cpu"):
        self.device = torch.device(device)
        self.model  = torch.jit.load(path, map_location=self.device)
        self.model.eval()

    @torch.no_grad()
    def infer(self, frame_bgr):
        # frame_bgr: np.ndarray (H,W,3) BGR 0–255
        img = torch.from_numpy(frame_bgr[:, :, ::-1].copy()).float() / 255.0
        img = img.permute(2,0,1).unsqueeze(0).to(self.device)  # B,C,H,W
        probs = self.model(img).softmax(1).squeeze(0).cpu().numpy()
        return probs
