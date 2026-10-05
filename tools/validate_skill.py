"""Check portable skill metadata and bundled file links, not artistic quality."""
from pathlib import Path
import argparse
import re
from urllib.parse import unquote, urlsplit

import yaml


def validate_skill(directory: Path) -> list[str]:
    root = directory.resolve()
    entry = root/'SKILL.md'
    errors: list[str] = []
    if not entry.is_file():
        return [f'{entry}: missing SKILL.md']
    try:
        content = entry.read_text(encoding='utf-8')
    except (OSError, UnicodeError) as error:
        return [f'{entry}: cannot read UTF-8: {error}']
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)',content,re.S)
    if not match:
        errors.append('SKILL.md: missing YAML frontmatter')
    else:
        try:
            metadata = yaml.safe_load(match.group(1))
        except yaml.YAMLError as error:
            errors.append(f'SKILL.md: invalid YAML: {error}')
        else:
            if not isinstance(metadata,dict):
                errors.append('SKILL.md: frontmatter must be a mapping')
            else:
                name = metadata.get('name')
                if not isinstance(name,str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',name) or len(name)>64:
                    errors.append('SKILL.md: invalid skill name')
                elif name!=root.name:
                    errors.append('SKILL.md: name must match directory name')
                description = metadata.get('description')
                if not isinstance(description,str) or not description.strip() or len(description)>1024:
                    errors.append('SKILL.md: description must be a nonempty string of at most 1024 characters')
                extra = metadata.get('metadata',{})
                if not isinstance(extra,dict) or any(not isinstance(k,str) or not isinstance(v,str) for k,v in extra.items()):
                    errors.append('SKILL.md: metadata must map strings to strings')
    for document in sorted(root.rglob('*.md')):
        relative = document.relative_to(root)
        if not document.resolve().is_relative_to(root):
            errors.append(f'{relative}: document escapes skill directory')
            continue
        try:
            text = document.read_text(encoding='utf-8')
        except (OSError,UnicodeError) as error:
            errors.append(f'{relative}: cannot read UTF-8: {error}')
            continue
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',text):
            target = target.strip()
            if not target or target.startswith('#'):
                continue
            if re.match(r'^[A-Za-z]:[\\/]',target):
                errors.append(f'{relative}: absolute platform path: {target}')
                continue
            url = urlsplit(target)
            if url.scheme in ('https','http','mailto'):
                continue
            if url.scheme or url.netloc:
                errors.append(f'{relative}: unsupported link scheme: {target}')
                continue
            destination = (document.parent/unquote(url.path)).resolve()
            if not destination.is_relative_to(root):
                errors.append(f'{relative}: link escapes skill directory: {target}')
            elif not destination.exists():
                errors.append(f'{relative}: missing local link: {target}')
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',nargs='?',type=Path,
                        default=Path(__file__).resolve().parents[1]/'skills/cionejr')
    args = parser.parse_args(argv)
    errors = validate_skill(args.directory)
    if errors:
        for error in errors:
            print(f'FAIL: {error}')
        return 1
    print(f'PASS: {args.directory} metadata and local links')
    print('Not checked: external URLs, anchor fragments, host discovery, or drawing quality.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
