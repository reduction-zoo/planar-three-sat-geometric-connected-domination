import AppKit
import PDFKit
import Foundation
let document = PDFDocument(url: URL(fileURLWithPath: CommandLine.arguments[1]))!
let destination = URL(fileURLWithPath: CommandLine.arguments[2], isDirectory: true)
try FileManager.default.createDirectory(at: destination, withIntermediateDirectories: true)
for index in 0..<document.pageCount {
    let page = document.page(at: index)!
    let box = page.bounds(for: .mediaBox)
    let thumbnail = page.thumbnail(of: NSSize(width: box.width * 1.5, height: box.height * 1.5), for: .mediaBox)
    let bitmap = NSBitmapImageRep(data: thumbnail.tiffRepresentation!)!
    let png = bitmap.representation(using: .png, properties: [:])!
    try png.write(to: destination.appendingPathComponent("page-\(index + 1).png"))
    print("page \(index + 1): \(Int(box.width)) x \(Int(box.height)) pt")
}
print("Rendered \(document.pageCount) pages")
