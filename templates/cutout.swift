// cutout — máscara de sujeto con Vision (macOS). Reemplaza ~/bin/cutout.
// uso: cutout <entrada.jpg> <salida.png> [--mask]
import Foundation
import Vision
import CoreImage
import AppKit

let args = CommandLine.arguments
guard args.count >= 3 else { FileHandle.standardError.write("uso: cutout in.jpg out.png [--mask]\n".data(using:.utf8)!); exit(2) }
let inPath = args[1], outPath = args[2]
let maskOnly = args.contains("--mask")

guard let src = CIImage(contentsOf: URL(fileURLWithPath: inPath)) else { print("no se pudo leer"); exit(1) }
let handler = VNImageRequestHandler(ciImage: src, options: [:])
let req = VNGenerateForegroundInstanceMaskRequest()
do { try handler.perform([req]) } catch { print("vision falló: \(error)"); exit(1) }
guard let obs = req.results?.first else { print("sin sujeto"); exit(1) }

let ctx = CIContext()
let pixels: CVPixelBuffer
do {
    pixels = try obs.generateScaledMaskForImage(forInstances: obs.allInstances, from: handler)
} catch { print("máscara falló: \(error)"); exit(1) }

var out = CIImage(cvPixelBuffer: pixels)
// escalar la máscara al tamaño original
let sx = src.extent.width / out.extent.width, sy = src.extent.height / out.extent.height
out = out.transformed(by: CGAffineTransform(scaleX: sx, y: sy))

let final: CIImage
if maskOnly {
    final = out   // escala de grises: blanco = sujeto
} else {
    final = src.applyingFilter("CIBlendWithMask", parameters: [kCIInputMaskImageKey: out])
}
guard let cg = ctx.createCGImage(final, from: src.extent) else { print("render falló"); exit(1) }
let rep = NSBitmapImageRep(cgImage: cg)
guard let data = rep.representation(using: .png, properties: [:]) else { print("png falló"); exit(1) }
try data.write(to: URL(fileURLWithPath: outPath))
print("ok \(outPath)")
