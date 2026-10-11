// ocr — detecta texto dentro de una imagen con Vision (macOS). Sin dependencias externas.
// uso:  ocr <imagen.png> [--min-conf 0.3]
// sale: JSON  {"count":N,"area":0.0-1.0,"items":[{"text":"...","conf":0.9,"box":[x,y,w,h]}]}
//
// Para qué: las fotos generadas por IA vuelven con letras inventadas (legends de teclas,
// pseudo-código en pantallas, escritura en papeles). Los prompts que piden "no text" NO
// alcanzan — se comprobó en el test de ads jul-2026: 8 de 14 fotos traían basura.
// Este binario permite hacerlo determinista (RUBRIC A11) en vez de dejarlo al ojo.
import Foundation
import Vision
import AppKit

let args = CommandLine.arguments
guard args.count >= 2 else {
    FileHandle.standardError.write("uso: ocr imagen.png [--min-conf 0.3]\n".data(using: .utf8)!)
    exit(2)
}
let inPath = args[1]
var minConf: Float = 0.3
if let i = args.firstIndex(of: "--min-conf"), i + 1 < args.count, let v = Float(args[i + 1]) { minConf = v }

guard let img = NSImage(contentsOfFile: inPath),
      let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    FileHandle.standardError.write("no se pudo leer \(inPath)\n".data(using: .utf8)!)
    exit(1)
}

let req = VNRecognizeTextRequest()
req.recognitionLevel = .accurate
// sin corrección de idioma: buscamos glifos, no palabras válidas. La basura de IA no es
// un idioma — si se corrige, Vision la descarta y el chequeo se vuelve ciego.
req.usesLanguageCorrection = false
req.recognitionLanguages = ["es-ES", "en-US"]

let handler = VNImageRequestHandler(cgImage: cg, options: [:])
do { try handler.perform([req]) } catch {
    FileHandle.standardError.write("vision falló: \(error)\n".data(using: .utf8)!)
    exit(1)
}

var items: [[String: Any]] = []
var area: Double = 0
for obs in (req.results ?? []) {
    guard let top = obs.topCandidates(1).first, top.confidence >= minConf else { continue }
    let b = obs.boundingBox              // normalizado, origen abajo-izquierda
    area += Double(b.width * b.height)
    items.append([
        "text": top.string,
        "conf": Double(top.confidence),
        // se convierte a origen arriba-izquierda, que es como razona el resto del pipeline
        "box": [Double(b.minX), Double(1 - b.maxY), Double(b.width), Double(b.height)],
    ])
}

let out: [String: Any] = ["count": items.count, "area": area, "items": items]
let data = try! JSONSerialization.data(withJSONObject: out, options: [.prettyPrinted, .sortedKeys])
FileHandle.standardOutput.write(data)
FileHandle.standardOutput.write("\n".data(using: .utf8)!)
