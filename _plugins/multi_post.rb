require 'cgi'

module Jekyll
  module PermalinkBuilder
    extend self

    def get_adjusted_permalink(resource, layout)
      layout_path = CGI.escape(layout)
      url = resource.url
      ext = File.extname(url)
      
      # Extract the post name (last part of the URL)
      post_name = url.split('/').last
      post_name = post_name.gsub(ext, '') if !ext.empty?
      
      if url.include?(':layout')
        return url.gsub(/:layout/, layout_path)
      end

      # Special case for 'post' layout - use clean URL
      if layout == 'post'
        return "/#{post_name}/"
      end

      # For other layouts like slideshow, append the layout name
      return "/#{post_name}/#{layout_path}/"
    end
  end

  class PageLayoutsGenerator
    def generate(site)
      pages = site.pages.map! do |page|
        if page.data["layout"].is_a?(Array)
          create_layout_views(page)
        else
          page
        end
      end

      pages.flatten!
    end

    private

    def create_layout_views(page)
      page.data["layout"].map do |layout|
        dir = File.dirname(page.relative_path)
        Page.new(page.site, page.site.source, dir, page.name).tap do |new_page|
          new_page.data["layout"] = layout
          new_page.data["permalink"] = PermalinkBuilder.get_adjusted_permalink(page, layout)
          
          # Add redirect from /post_name/post/ to /post_name/ for backward compatibility
          if layout == 'post'
            # Extract post_name from permalink
            post_name = new_page.data["permalink"].split('/').reject(&:empty?).last
            
            # Initialize redirect_from array if it doesn't exist
            new_page.data["redirect_from"] ||= []
            
            # Add redirect from /post_name/post/ to /post_name/
            new_page.data["redirect_from"] << "/#{post_name}/post/"
          end
        end
      end
    end
  end

  class CollectionLayoutsGenerator
    def generate(site)
      site.collections.each do |_, collection|
        docs = collection.docs.map! do |doc|
          if doc.data["layout"].is_a?(Array)
            create_layout_views(site, collection, doc)
          else
            doc
          end
        end

        docs.flatten!
      end
    end

    private

    def create_layout_views(site, collection, doc)
      doc.data["layout"].map do |layout|
        Document.new(doc.path, :site => site, :collection => collection).tap do |new_doc|
          new_doc.read
          new_doc.data["layout"] = layout
          new_doc.data["permalink"] = PermalinkBuilder.get_adjusted_permalink(doc, layout)
          
          # Add redirect from /post_name/post/ to /post_name/ for backward compatibility
          if layout == 'post'
            # Extract post_name from permalink
            post_name = new_doc.data["permalink"].split('/').reject(&:empty?).last
            
            # Initialize redirect_from array if it doesn't exist
            new_doc.data["redirect_from"] ||= []
            
            # Add redirect from /post_name/post/ to /post_name/
            new_doc.data["redirect_from"] << "/#{post_name}/post/"
          end
        end
      end
    end
  end

  class MultiPostGenerator < Generator
    safe true

    def generate(site)
      PageLayoutsGenerator.new.generate(site)
      CollectionLayoutsGenerator.new.generate(site)
    end
  end
end
