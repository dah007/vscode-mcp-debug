from importlib import import_module

# Import the FastAPI app from server.main
mod = import_module('server.main')
app = mod.app

print('Top-level routes:')
for r in app.routes:
    try:
        print(type(r).__name__, getattr(r, 'path', getattr(r, 'path_template', r)) )
    except Exception as e:
        print('Route:', r, 'error printing path:', e)

# If there is a mounted subapp at '/sse', print its routes too
for r in app.routes:
    if getattr(r, 'path', None) == '/sse':
        subapp = getattr(r, 'app', None)
        if subapp:
            print('\nMounted /sse subapp routes:')
            for sr in getattr(subapp, 'routes', []):
                try:
                    print(type(sr).__name__, getattr(sr, 'path', getattr(sr, 'path_template', sr)))
                except Exception as e:
                    print('Subroute:', sr, 'error:', e)
            break
else:
    print('\nNo explicit /sse mount found in app.routes')
