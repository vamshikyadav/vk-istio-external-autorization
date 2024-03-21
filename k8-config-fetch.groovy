def folderPath = '/path/to/your/folder'
def keyPath = "some.key.path"
def configMapName = "my-configmap"

def folder = new File(folderPath)

folder.eachFile { file ->
    if (file.isFile() && file.name.endsWith(".yaml")) {
        def command = "kubectl create configmap $configMapName --from-file=${file.absolutePath} --dry-run=client -o json | jq -r '.data.\"${file.name}\"' | yq r - $keyPath"
        def value = command.execute().text.trim()

        println "File name: ${file.name}, Value of '$keyPath': $value"
    }
}