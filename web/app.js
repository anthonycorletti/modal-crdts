/* eslint-env browser */

import * as Y from 'yjs'
import { WebsocketProvider } from 'y-websocket'
import { QuillBinding } from 'y-quill'
import Quill from 'quill'
import QuillCursors from 'quill-cursors'
import { uniqueNamesGenerator, adjectives, animals } from 'unique-names-generator'


Quill.register('modules/cursors', QuillCursors)

window.addEventListener('load', () => {
    const ydoc = new Y.Doc()
    const provider = new WebsocketProvider(
        `ws${location.protocol.slice(4)}//${location.host}/ws`,
        'quill-demo',
        ydoc
    )
    const ytext = ydoc.getText('quill')
    const editorContainer = document.getElementById('editor')
    editorContainer.setAttribute('id', 'editor')
    document.body.insertBefore(editorContainer, null)

    const editor = new Quill(editorContainer, {
        modules: {
            cursors: true,
            toolbar: [
                [{ header: [1, 2, false] }],
                ['bold', 'italic', 'underline'],
                ['image', 'code-block', 'link'],
                [{ list: 'ordered' }, { list: 'bullet' }],
                ['clean']
            ],
            history: {
                userOnly: true
            }
        },
        placeholder: 'Start writing...',
        theme: 'snow' // or 'bubble'
    })

    const binding = new QuillBinding(ytext, editor, provider.awareness)

    provider.awareness.setLocalStateField('user', {
        name: uniqueNamesGenerator({ dictionaries: [adjectives, animals] }),
        color: `#${Array.from({ length: 3 }, () => ('0' + Math.floor(Math.random() * 128).toString(16)).slice(-2)).join('')}`
    })

    window.example = { provider, ydoc, ytext, binding, Y }
})
