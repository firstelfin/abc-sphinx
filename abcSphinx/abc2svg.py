import os
import subprocess
import hashlib
import tempfile
import shutil
from pathlib import Path
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.application import Sphinx
from sphinx.util import logging
from sphinx.util.fileutil import copy_asset_file

logger = logging.getLogger(__name__)


def copy_abc_assets(app, exception):
    """复制ABC扩展的静态资源文件"""
    if exception:
        # 如果有构建异常，跳过资源复制
        logger.warning("Exception occurred, skipping ABC assets copy")
        return
    
    # 获取源CSS文件路径
    src_dir = os.path.dirname(__file__)
    css_src = os.path.join(src_dir, "abc.css")
    
    # 目标目录
    static_dir = os.path.join(app.outdir, "_static")
    
    # 确保目标目录存在
    os.makedirs(static_dir, exist_ok=True)
    
    # 检查源文件是否存在
    if os.path.isfile(css_src):
        try:
            # 复制CSS文件
            copy_asset_file(css_src, static_dir)
            logger.info(f"Copied ABC CSS to {static_dir}")
        except Exception as e:
            logger.warning(f"Failed to copy ABC CSS: {str(e)}")
    else:
        logger.warning(f"ABC CSS file not found: {css_src}")


def ensure_svg_background(svg_path):
    """确保 SVG 文件有白色背景"""
    try:
        with open(svg_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 如果已经有 background 样式，跳过
        if 'background' in content or 'rect' in content:
            return

        # 在 <svg> 标签内插入 style 属性
        if '<svg' in content:
            content = content.replace(
                '<svg',
                '<svg style="background: white;"',
                1
            )
            # 或者插入一个白色矩形（更可靠）
            # content = content.replace(
            #     '<svg',
            #     '<svg><rect width="100%" height="100%" fill="white"/>',
            #     1
            # )

        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        logger.warning(f"Failed to add background to SVG: {e}")


class ABCDirective(Directive):
    """Sphinx directive for rendering ABC music notation"""
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    has_content = True
    
    option_spec = {
        'staffwidth': int,
        'scale': float,
        'voicebreak': int,
        'landscape': bool,
    }

    def run(self):
        # 获取ABC代码内容
        logger.info(f"Rendering ABC starting...")
        abc_content = '\n'.join(self.content)
        
        if not abc_content.strip():
            return [nodes.error(text="ABC directive has no content")]
        
        # 获取指令选项
        options = self.options
        staffwidth = options.get('staffwidth', '600pt')  # 默认谱表宽度
        scale = options.get('scale', 1.0)          # 默认缩放比例
        voicebreak = options.get('voicebreak', 0)   # 默认声部间距
        landscape = 'landscape' in options         # 是否横向布局
        
        # 生成唯一文件名
        content_hash = hashlib.md5(abc_content.encode()).hexdigest()[:10]
        filename = f"abc_{content_hash}.svg"
        
        # 获取构建环境
        env = self.state.document.settings.env
        # build_dir = Path(env.app.outdir)
        static_dir = Path(env.app.outdir) / "_static"
        images_dir = static_dir / "_abc_images"
        images_dir.mkdir(parents=True, exist_ok=True)
        
        svg_path = images_dir / filename
        
        # 检查是否已存在渲染结果
        if not svg_path.exists() or env.config.abc_force_rebuild:
            try:
                # 创建临时目录
                with tempfile.TemporaryDirectory() as tmpdir:
                    tmp_path = Path(tmpdir)
                    
                    # 生成ABC文件
                    abc_file = tmp_path / "input.abc"
                    with abc_file.open('w') as f:
                        f.write(abc_content)
                    
                    # 构建abcm2ps命令
                    logger.info(f"Rendering ABC to SVG: {abc_file}")
                    cmd = [
                        "abcm2ps",
                        "-g",  # 生成SVG格式
                        f"-O{tmp_path}/output",
                        abc_file
                    ]
                    
                    # 添加选项
                    if staffwidth:
                        cmd.extend(["-w", str(staffwidth)])
                    if scale:
                        cmd.extend(["-s", str(scale)])
                    if voicebreak:
                        cmd.extend(["-b", str(voicebreak)])
                    if landscape:
                        cmd.extend(["-l"])
                    
                    # 执行渲染
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        cwd=tmpdir
                    )
                    
                    if result.returncode != 0:
                        error_msg = f"abcm2ps failed: {result.stderr}"
                        logger.error(error_msg)
                        return [nodes.error(text=error_msg)]
                    
                    # 查找生成的SVG文件
                    svg_files = list(tmp_path.glob("output*.svg"))
                    if not svg_files:
                        error_msg = "No SVG file generated by abcm2ps"
                        logger.error(error_msg)
                        return [nodes.error(text=error_msg)]
                    
                    # 复制到最终位置
                    shutil.copy(svg_files[0], svg_path)
                    ensure_svg_background(svg_path)
            
            except FileNotFoundError:
                error_msg = "abcm2ps not found. Please install it: https://abc.sourceforge.net/abcMIDI/#abcm2ps"
                logger.error(error_msg)
                return [nodes.error(text=error_msg)]
            except Exception as e:
                error_msg = f"ABC rendering error: {str(e)}"
                logger.error(error_msg)
                return [nodes.error(text=error_msg)]
        
        # 创建图像节点

        raw_html = (
            f'<div class="abc-container">\n'
            f'  <img src="/_static/_abc_images/{filename}" '
            f'class="abc-rendered" alt="abc music - {filename}" />\n'
            f'</div>'
        )

        # 创建 raw 节点，指定为 HTML
        raw_node = nodes.raw('', raw_html, format='html')

        # 如果有标题，用 figure 包裹
        if self.arguments:
            caption = nodes.caption(text=self.arguments[0])
            figure_node = nodes.figure('', raw_node, caption)
            return [figure_node]

        return [raw_node]
    

def setup(app: Sphinx):
    """Setup the ABC extension"""
    app.add_directive("abc", ABCDirective)
    
    # 添加配置选项
    app.add_config_value("abc_force_rebuild", False, "env")
    
    # 创建输出目录
    app.connect("builder-inited", lambda app: os.makedirs(
        os.path.join(app.outdir, "_abc_images"), exist_ok=True))
    
    # 复制CSS资源
    app.connect("build-finished", copy_abc_assets)
    
    # 添加CSS
    app.add_css_file("abc.css")
    
    return {
        'version': '0.2',
        'parallel_read_safe': True,
        'parallel_write_safe': True
    }